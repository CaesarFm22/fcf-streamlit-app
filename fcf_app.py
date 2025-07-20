import streamlit as st
import requests
import json

# App settings
st.set_page_config(page_title="Caesar's Quick Value Finder", layout="centered")
st.title("🏛️ Caesar's Quick Value Finder")
st.markdown("Enter a stock ticker to estimate intrinsic value using discounted cash flow (DCF) analysis.")

# Get secrets
api_key = st.secrets["API_KEY"]
api_url = st.secrets["API_URL"]

# User inputs
ticker = st.text_input("Enter stock ticker (e.g., AAPL)").upper()
cagr = st.slider("Expected FCF Growth Rate (CAGR %)", min_value=0, max_value=20, value=5)

if st.button("Calculate"):
    if not ticker:
        st.warning("Please enter a valid ticker.")
    else:
        with st.spinner("Requesting valuation..."):
            try:
                # Prepare headers and params
                headers = {"x-api-key": api_key}
                params = {"ticker": ticker, "cagr": cagr}

                # Send request to FastAPI backend
                response = requests.get(api_url, headers=headers, params=params)

                if response.status_code == 200:
                    data = response.json()
                    st.success("Valuation Complete!")
                    st.write(f"**Free Cash Flow (FCF):** ${data['fcf']:,}")
                    st.write(f"**FCF per Share:** ${data['fcf_per_share']:.2f}")
                    st.write(f"**DCF Intrinsic Value per Share:** ${data['dcf_per_share']:.2f}")

                    st.subheader("📈 Projected FCF (Next 10 Years)")
                    st.line_chart(data["projected_fcf"])
                else:
                    st.error(f"Error {response.status_code}: {response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {e}")
            except json.JSONDecodeError:
                st.error("Invalid response format from backend.")
