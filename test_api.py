"""
Test script for the deployed Churn Prediction API
Run this after starting the API to verify everything works
"""

import requests

BASE_URL = "http://localhost:8000"

def test_health():
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health Check: {response.json()}")
    assert response.status_code == 200

def test_predict_high_risk():
    """High risk: short tenure, month-to-month contract"""
    payload = {
        "tenure": 2,
        "monthly_charges": 85.0,
        "total_charges": 170.0,
        "contract_type": "Month-to-month"
    }
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    result = response.json()
    print(f"\nHigh Risk Customer: {result}")
    assert response.status_code == 200

def test_predict_low_risk():
    """Low risk: long tenure, two year contract"""
    payload = {
        "tenure": 60,
        "monthly_charges": 45.0,
        "total_charges": 2700.0,
        "contract_type": "Two year"
    }
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    result = response.json()
    print(f"\nLow Risk Customer: {result}")
    assert response.status_code == 200

def test_invalid_input():
    """Should return 422 for invalid input"""
    payload = {
        "tenure": -5,          # invalid: negative
        "monthly_charges": 50.0,
        "total_charges": 100.0,
        "contract_type": "Month-to-month"
    }
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    print(f"\nInvalid Input Test: Status {response.status_code}")
    assert response.status_code == 422

def test_model_info():
    response = requests.get(f"{BASE_URL}/model-info")
    print(f"\nModel Info: {response.json()}")
    assert response.status_code == 200

if __name__ == "__main__":
    print("Testing Churn Prediction API...\n" + "="*50)
    test_health()
    test_predict_high_risk()
    test_predict_low_risk()
    test_invalid_input()
    test_model_info()
    print("\n" + "="*50)
    print("✅ All tests passed!")
