import streamlit as st
import requests

# Configuration
API_URL = "https://render-om30.onrender.com/calculate"
API_KEY = "barakliliyasha!@"

st.set_page_config(page_title="FCF Valuation App")
st.title("📈 Free Cash Flow Valuation")

# User Inputs
ticker = st.text_input("Enter Ticker Symbol", value="AAPL")
cagr = st.slider("Select CAGR (%)", min_value=0, max_value=30, value=10)

# Button
if st.button("Calculate Valuation"):
    try:
        # Make GET request to FastAPI with API Key in headers
        response = requests.get(
            API_URL,
            params={"ticker": ticker, "cagr": cagr},
            headers={"x-api-key": API_KEY}
        )

        if response.status_code == 200:
            valuation = response.json().get("valuation")
            st.success(f"✅ {valuation}")
        elif response.status_code == 403:
            st.error("❌ Error 403: Invalid API Key")
        else:
            st.error(f"❌ Error {response.status_code}: {response.text}")

    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
