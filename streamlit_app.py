#Section 1
import streamlit as st
import requests
import json

# Page configuration
st.set_page_config(
       page_title="Churn Prediction Dashboard",
       page_icon="📊",
       layout="wide"
       )
       
#Title
st.title("📊 Customer Churn Prediction Dashboard")
st.markdown("Predict whether a customer is likely to churn based on their profile.")
st.divider()

#Section 2:Customer Input Form

st.subheader("Customer Profile")

col1, col2, col3 = st.columns(3)

with col1:
    tenure= st.slider("Tenure (months)", 0, 72, 12)
    monthly_charges= st.slider("Monthly Charges ($)", 18,120, 65)
    senior_citizen= st.selectbox("Senior Citizen", [0,1])
    partner= st.selectbox("Has Partner", [0,1])
    dependents = st.selectbox("Has Dependents", [0,1])
    
with col2:
    contract = st.selectbox(
      "Contract Type",
      ["Month-to-month", "One year", "Two year"]
    )
    internet_service = st.selectbox(
      "Internet Service",
      ["DSL", "Fiber optic", "No"]
    )
    payment_method= st.selectbox(
     "Payment Method",
     ["Electronic check", "Mailed check",
      "Bank transfer (automatic)",
      "Credit card (automatic)"]
     )

with col3:
    tech_support = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
    online_security= st.selectbox("Online Security", ["No", "Yes", "No intenret service"])
    phone_service = st.selectbox("Phone Service", [1,0])
    paperless_billing = st.selectbox("Paperless Billing", [1,0])

#Section 3- Encode inputs and make prediction:
# Section 3 - Encode inputs and predict
st.divider()

if st.button("🔮 Predict Churn", type="primary"):
    
    # Encode contract type
    contract_one_year = 1 if contract == "One year" else 0
    contract_two_year = 1 if contract == "Two year" else 0
    
    # Encode internet service
    internet_fiber = 1 if internet_service == "Fiber optic" else 0
    internet_no = 1 if internet_service == "No" else 0
    
    # Encode payment method
    pay_credit = 1 if payment_method == "Credit card (automatic)" else 0
    pay_electronic = 1 if payment_method == "Electronic check" else 0
    pay_mailed = 1 if payment_method == "Mailed check" else 0
    
    # Encode tech support and online security
    tech_no_internet = 1 if tech_support == "No internet service" else 0
    tech_yes = 1 if tech_support == "Yes" else 0
    sec_no_internet = 1 if online_security == "No internet service" else 0
    sec_yes = 1 if online_security == "Yes" else 0

    # Build the customer profile payload
    payload = {
        "gender": 1,
        "SeniorCitizen": senior_citizen,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": float(tenure),
        "PhoneService": phone_service,
        "PaperlessBilling": paperless_billing,
        "MonthlyCharges": float(monthly_charges),
        "MultipleLines_No_phone_service": 0,
        "MultipleLines_Yes": 0,
        "InternetService_Fiber_optic": internet_fiber,
        "InternetService_No": internet_no,
        "OnlineSecurity_No_internet_service": sec_no_internet,
        "OnlineSecurity_Yes": sec_yes,
        "OnlineBackup_No_internet_service": 0,
        "OnlineBackup_Yes": 0,
        "DeviceProtection_No_internet_service": 0,
        "DeviceProtection_Yes": 0,
        "TechSupport_No_internet_service": tech_no_internet,
        "TechSupport_Yes": tech_yes,
        "StreamingTV_No_internet_service": 0,
        "StreamingTV_Yes": 0,
        "StreamingMovies_No_internet_service": 0,
        "StreamingMovies_Yes": 0,
        "Contract_One_year": contract_one_year,
        "Contract_Two_year": contract_two_year,
        "PaymentMethod_Credit_card_automatic": pay_credit,
        "PaymentMethod_Electronic_check": pay_electronic,
        "PaymentMethod_Mailed_check": pay_mailed
    }

    # Send to FastAPI
    try:
        response = requests.post(
            "http://localhost:8000/predict",
            json=payload
        )
        result = response.json()
        
        # Display results
        st.divider()
        col_result1, col_result2 = st.columns(2)
        
        with col_result1:
            probability = result['churn_probability'] * 100
            st.metric(
                label="Churn Probability",
                value=f"{probability:.1f}%"
            )
            
        with col_result2:
            prediction = result['prediction']
            if prediction == "High Risk":
                st.error(f"⚠️ {prediction}")
            else:
                st.success(f"✅ {prediction}")
        
        st.info(result['message'])
        
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        st.warning("Make sure the FastAPI server is running on port 8000")    
