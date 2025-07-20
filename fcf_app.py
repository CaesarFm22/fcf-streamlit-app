import streamlit as st
import requests
import os

# BACKEND URL (change to your actual deployed FastAPI URL)
API_URL = "https://render-om30.onrender.com/calculate"

# Store the API key securely in Streamlit Secrets or directly here for testing
API_KEY = st.secrets["API_KEY"] if "API_KEY" in st.secrets else os.getenv("API_KEY")

st.set_page_config(page_title="Valuation Calculator", layout="centered")

st.title("📈 Stock Valuation Estimator")

# Input fields
ticker = st.text_input("Enter Stock Ticker", value="AAPL")
cagr = st.number_input("Enter CAGR (%)", min_value=0.0, step=0.1, value=5.0)

# Submit button
if st.button("Calculate Valuation"):
    if not API_KEY:
        st.error("API key not found. Please configure it in Streamlit secrets or environment.")
    else:
        try:
            response = requests.get(
                API_URL,
                params={"ticker": ticker, "cagr": cagr},
                headers={"x-api-key": API_KEY}
            )
            if response.status_code == 200:
                result = response.json()
                st.success(f"✅ {result['valuation']}")
            else:
                st.error(f"❌ Error: {response.status_code} - {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"⚠️ Request failed: {e}")
