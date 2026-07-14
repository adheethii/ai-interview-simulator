"""
Train and save the Telecom Churn prediction model.
Run this once to generate model.pkl before deploying the API.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, f1_score, roc_auc_score
from imblearn.over_sampling import SMOTE
import pickle

# ─────────────────────────────────────────────
# 1. Load Data
# ─────────────────────────────────────────────
# Replace with your actual dataset path
df = pd.read_csv("telecom_churn.csv")

# ─────────────────────────────────────────────
# 2. Feature Engineering
# ─────────────────────────────────────────────

# Encode categorical variables
le_contract = LabelEncoder()
df["Contract_encoded"] = le_contract.fit_transform(df["Contract"])

# Select features used in the API
FEATURES = ["tenure", "MonthlyCharges", "TotalCharges", "Contract_encoded"]
TARGET = "Churn"

# Handle missing values
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df["TotalCharges"].fillna(df["TotalCharges"].median(), inplace=True)

X = df[FEATURES]
y = df[TARGET].map({"Yes": 1, "No": 0})

# ─────────────────────────────────────────────
# 3. Train/Test Split
# ─────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ─────────────────────────────────────────────
# 4. Scale Features
# ─────────────────────────────────────────────
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ─────────────────────────────────────────────
# 5. Handle Class Imbalance with SMOTE
# ─────────────────────────────────────────────
smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train_scaled, y_train)

print(f"Before SMOTE: {y_train.value_counts().to_dict()}")
print(f"After SMOTE:  {pd.Series(y_train_balanced).value_counts().to_dict()}")

# ─────────────────────────────────────────────
# 6. Train Model
# ─────────────────────────────────────────────
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    random_state=42
)
model.fit(X_train_balanced, y_train_balanced)

# ─────────────────────────────────────────────
# 7. Cross Validation
# ─────────────────────────────────────────────
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(model, X_train_balanced, y_train_balanced, cv=skf, scoring="f1")
print(f"\nCross-Validation F1: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

# ─────────────────────────────────────────────
# 8. Evaluate on Test Set
# ─────────────────────────────────────────────
y_pred = model.predict(X_test_scaled)
y_proba = model.predict_proba(X_test_scaled)[:, 1]

print("\n" + "="*50)
print("TEST SET PERFORMANCE")
print("="*50)
print(classification_report(y_test, y_pred))
print(f"F1 Score: {f1_score(y_test, y_pred):.3f}")
print(f"ROC-AUC:  {roc_auc_score(y_test, y_proba):.3f}")

# ─────────────────────────────────────────────
# 9. Feature Importance
# ─────────────────────────────────────────────
importance = pd.DataFrame({
    "feature": FEATURES,
    "importance": model.feature_importances_
}).sort_values("importance", ascending=False)
print("\nFeature Importance:")
print(importance)

# ─────────────────────────────────────────────
# 10. Save Model, Scaler, and Encoder
# ─────────────────────────────────────────────
artifacts = {
    "model": model,
    "scaler": scaler,
    "contract_encoder": le_contract,
    "features": FEATURES
}

with open("model.pkl", "wb") as f:
    pickle.dump(artifacts, f)

print("\n✅ Model saved as model.pkl")
