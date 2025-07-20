# fcf_app.py
import streamlit as st
import requests

st.title("FCF Valuation App")

api_url = "https://render-om30.onrender.com/calculate"  # your deployed FastAPI URL
api_key = "barakliliyasha!@"  # don't hardcode this in production

ticker = st.text_input("Enter ticker:")
cagr = st.slider("CAGR (%)", min_value=0.0, max_value=20.0, value=5.0)

if st.button("Calculate Valuation"):
    if not ticker:
        st.error("Please enter a ticker.")
    else:
        try:
            response = requests.get(
                api_url,
                params={"ticker": ticker, "cagr": cagr},
                headers={"x-api-key": api_key}
            )
            if response.status_code == 200:
                st.success(f"Valuation: {response.json()['valuation']}")
            else:
                st.error(f"Error {response.status_code}: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"Connection error: {e}")
