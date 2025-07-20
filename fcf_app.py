import streamlit as st
import requests

# Page config
st.set_page_config(page_title="Caesar's Quick Value Finder", layout="centered")

st.title("📈 Caesar's Quick Value Finder")

# Input fields
ticker = st.text_input("Enter ticker symbol (e.g., AAPL):", value="AAPL")
cagr = st.slider("Expected CAGR (%)", min_value=0, max_value=30, value=5)

if st.button("Calculate DCF Valuation"):
    if not ticker:
        st.warning("Please enter a ticker symbol.")
    else:
        # Load API settings
        try:
            api_url = st.secrets["API_URL"]
            api_key = st.secrets["API_KEY"]
        except KeyError as e:
            st.error(f"Missing secret: {e}")
            st.stop()

        # Prepare request
        params = {"ticker": ticker, "cagr": cagr}
        headers = {"x-api-key": api_key}

        try:
            response = requests.get(api_url, headers=headers, params=params)
            st.write("Status code:", response.status_code)  # Debug
            st.write("Raw response:", response.text)        # Debug

            if response.status_code == 200:
                data = response.json()

                st.success("Valuation calculated successfully!")
                st.metric("Free Cash Flow (FCF)", f"${data['fcf']:,}")
                st.metric("FCF per Share", f"${data['fcf_per_share']:.2f}")
                st.metric("DCF per Share", f"${data['dcf_per_share']:.2f}")

                st.subheader("Projected FCF (Next 10 Years)")
                st.line_chart(data['projected_fcf'])

            else:
                st.error(f"Error {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {e}")
