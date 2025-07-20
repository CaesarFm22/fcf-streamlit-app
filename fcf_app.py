import streamlit as st
import requests

st.title("Valuation Calculator")

ticker = st.text_input("Enter stock ticker", value="AAPL")
cagr = st.number_input("Enter CAGR (%)", value=10.0)

if st.button("Calculate Valuation"):
    api_url = "https://render-om30.onrender.com/calculate"
    headers = {"x-api-key": "barakliliyasha!@"}
    params = {"ticker": ticker, "cagr": cagr}
    
    try:
        response = requests.get(api_url, headers=headers, params=params)
        if response.status_code == 200:
            result = response.json()
            st.success(f"✅ {result['valuation']}")
        else:
            st.error(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"⚠️ Exception occurred: {e}")
