# Section 1 - Imports and loading
import pickle
import numpy as np
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Load model, scaler and feature names once at startup
with open('best_xgb_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

with open('feature_names.pkl', 'rb') as f:
    feature_names = pickle.load(f)

# Create FastAPI app
app = FastAPI(title="Churn Prediction API")
print("Model loaded successfully")

# Section 2 - Pydantic schema
class CustomerProfile(BaseModel):
    gender: int
    SeniorCitizen: int
    Partner: int
    Dependents: int
    tenure: float
    PhoneService: int
    PaperlessBilling: int
    MonthlyCharges: float
    MultipleLines_No_phone_service: int
    MultipleLines_Yes: int
    InternetService_Fiber_optic: int
    InternetService_No: int
    OnlineSecurity_No_internet_service: int
    OnlineSecurity_Yes: int
    OnlineBackup_No_internet_service: int
    OnlineBackup_Yes: int
    DeviceProtection_No_internet_service: int
    DeviceProtection_Yes: int
    TechSupport_No_internet_service: int
    TechSupport_Yes: int
    StreamingTV_No_internet_service: int
    StreamingTV_Yes: int
    StreamingMovies_No_internet_service: int
    StreamingMovies_Yes: int
    Contract_One_year: int
    Contract_Two_year: int
    PaymentMethod_Credit_card_automatic: int
    PaymentMethod_Electronic_check: int
    PaymentMethod_Mailed_check: int

# Section 3 - Prediction endpoint
@app.post("/predict")
def predict_churn(customer: CustomerProfile):

    # Convert incoming data to dictionary
    data = customer.model_dump()

    # Create DataFrame with correct column order
    df = pd.DataFrame([data])

    # Rename columns to match training feature names
    df.columns = feature_names

    # Scale numerical columns
    df[['tenure', 'MonthlyCharges']] = scaler.transform(
        df[['tenure', 'MonthlyCharges']]
    )

    # Make prediction
    churn_probability = model.predict_proba(df)[0][1]
    prediction = "High Risk" if churn_probability >= 0.5 else "Low Risk"

    return {
        "churn_probability": round(float(churn_probability), 4),
        "prediction": prediction,
        "message": f"This customer has a {round(churn_probability*100, 1)}% chance of churning"
    }

# Section 4 - Running the server
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )       