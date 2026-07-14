"""
Telecom Customer Churn Prediction API
FastAPI application serving the trained Random Forest model.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pickle
import numpy as np
from typing import Literal

# ─────────────────────────────────────────────
# App Initialization
# ─────────────────────────────────────────────
app = FastAPI(
    title="Telecom Churn Prediction API",
    description="Predicts customer churn probability using a trained Random Forest model",
    version="1.0.0"
)

# ─────────────────────────────────────────────
# Load Model Artifacts at Startup
# ─────────────────────────────────────────────
try:
    with open("model.pkl", "rb") as f:
        artifacts = pickle.load(f)
    model = artifacts["model"]
    scaler = artifacts["scaler"]
    contract_encoder = artifacts["contract_encoder"]
    FEATURES = artifacts["features"]
    MODEL_LOADED = True
except FileNotFoundError:
    MODEL_LOADED = False
    print("⚠️ model.pkl not found. Run train_model.py first!")


# ─────────────────────────────────────────────
# Request/Response Models
# ─────────────────────────────────────────────

class CustomerData(BaseModel):
    tenure: int = Field(..., ge=0, le=100, description="Months as customer")
    monthly_charges: float = Field(..., gt=0, description="Monthly charge amount")
    total_charges: float = Field(..., ge=0, description="Total charges to date")
    contract_type: Literal["Month-to-month", "One year", "Two year"] = Field(
        ..., description="Type of contract"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "tenure": 24,
                "monthly_charges": 65.50,
                "total_charges": 1572.00,
                "contract_type": "Month-to-month"
            }
        }


class PredictionResponse(BaseModel):
    churn_prediction: str
    churn_probability: float
    risk_level: str


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool


# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────

@app.get("/", tags=["Info"])
def root():
    return {
        "message": "Telecom Churn Prediction API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Info"])
def health_check():
    return {
        "status": "healthy" if MODEL_LOADED else "model not loaded",
        "model_loaded": MODEL_LOADED
    }


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict_churn(data: CustomerData):
    if not MODEL_LOADED:
        raise HTTPException(status_code=503, detail="Model not loaded. Contact administrator.")

    try:
        # Encode contract type
        contract_encoded = contract_encoder.transform([data.contract_type])[0]

        # Prepare features in correct order
        features = np.array([[
            data.tenure,
            data.monthly_charges,
            data.total_charges,
            contract_encoded
        ]])

        # Scale features
        features_scaled = scaler.transform(features)

        # Predict
        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0][1]

        # Determine risk level
        if probability >= 0.7:
            risk_level = "High"
        elif probability >= 0.4:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        return {
            "churn_prediction": "Yes" if prediction == 1 else "No",
            "churn_probability": round(float(probability), 3),
            "risk_level": risk_level
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")


@app.get("/model-info", tags=["Info"])
def model_info():
    if not MODEL_LOADED:
        raise HTTPException(status_code=503, detail="Model not loaded")

    return {
        "model_type": "Random Forest Classifier",
        "features_used": FEATURES,
        "preprocessing": ["StandardScaler", "SMOTE (training only)"],
        "n_estimators": model.n_estimators,
        "max_depth": model.max_depth
    }
