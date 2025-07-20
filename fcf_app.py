import streamlit as st
import requests

# Set page config
st.set_page_config(page_title="Caesar's Quick Value Finder", layout="centered")

# Load API credentials from secrets
api_key = st.secrets["API_KEY"]
api_url = st.secrets["API_URL"]

# UI elements
st.title("Caesar's Quick Value Finder")
st.subheader("Estimate a stock's intrinsic value based on FCF and growth")

ticker = st.text_input("Enter Ticker Symbol", value="AAPL")
cagr = st.slider("Expected CAGR (%)", 0.0, 20.0, 5.0)

if st.button("Calculate Valuation"):
    with st.spinner("Fetching data and calculating..."):
        try:
            response = requests.get(
                f"{api_url}/calculate",
                params={"ticker": ticker, "cagr": cagr},
                headers={"x-api-key": api_key}
            )
            response.raise_for_status()
            data = response.json()

            st.success(f"DCF Value per Share: ${data['dcf_per_share']}")
            st.metric("FCF Per Share", f"${data['fcf_per_share']}")
            st.metric("FCF (Latest Year)", f"${data['fcf']}")

            st.subheader("Projected Free Cash Flow")
            st.line_chart(data["projected_fcf"])

        except requests.exceptions.HTTPError as http_err:
            st.error(f"API error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as req_err:
            st.error(f"Connection error: {req_err}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
