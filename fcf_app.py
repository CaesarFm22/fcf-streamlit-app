import streamlit as st
import requests

API_URL = "https://render-om30.onrender.com/calculate"
API_KEY = "barakliliyasha!@"

st.title("📊 FCF Valuation App")

ticker = st.text_input("Enter Ticker Symbol", "AAPL")
cagr = st.slider("Select Expected CAGR (%)", 0.0, 20.0, 10.0)

if st.button("Calculate Valuation"):
    with st.spinner("Calculating..."):
        try:
            response = requests.get(
                API_URL,
                params={"ticker": ticker, "cagr": cagr},
                headers={"x-api-key": API_KEY},
                timeout=10
            )
            if response.status_code == 200:
                result = response.json()
                st.success(f"✅ {result['valuation']}")
            else:
                st.error(f"❌ Error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"🚨 Connection error: {e}")
