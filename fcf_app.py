import streamlit as st
import requests

st.set_page_config(page_title="Caesar's Quick Value Finder", layout="centered")

st.title("📊 Caesar's Quick Value Finder")

ticker = st.text_input("Enter a stock ticker (e.g., AAPL, MSFT)")
cagr = st.slider("Expected CAGR (%)", min_value=0, max_value=20, value=5)

if "API_KEY" not in st.secrets:
    st.error("API key not found in secrets. Add it to `.streamlit/secrets.toml`.")
    st.stop()

api_key = st.secrets["API_KEY"]
api_url = "http://127.0.0.1:8000/calculate"  # Replace with your deployed backend if hosted remotely

if st.button("Calculate Valuation"):
    if not ticker:
        st.warning("Please enter a valid ticker.")
    else:
        try:
            headers = {"X-API-Key": api_key}
            params = {"ticker": ticker, "cagr": cagr}
            response = requests.get(api_url, params=params, headers=headers)

            if response.status_code == 200:
                data = response.json()
                st.success(f"Valuation for {ticker.upper()}")
                st.metric("FCF per Share", f"${data['fcf_per_share']:.2f}")
                st.metric("DCF per Share", f"${data['dcf_per_share']:.2f}")
                st.line_chart(data["projected_fcf"], height=300)
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {e}")
