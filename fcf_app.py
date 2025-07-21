import fcf_app as st
import requests

st.set_page_config(page_title="Caesar's Quick Value Finder", layout="centered")

st.title("🧠 Caesar's Quick Value Finder")

ticker = st.text_input("Enter Stock Ticker (e.g. AAPL)", value="AAPL")
cagr = st.number_input("Enter FCF Growth Rate (%)", min_value=0.0, max_value=50.0, value=5.0)
api_key = st.secrets.get("API_KEY", "your-secret-api-key")  # Store API key safely

if st.button("Get Valuation"):
    try:
        res = requests.get(
            "http://127.0.0.1:8000/calculate",
            params={"ticker": ticker, "cagr": cagr},
            headers={"x-api-key": api_key}
        )
        if res.status_code == 200:
            data = res.json()
            st.success(f"✅ FCF: ${data['fcf']:,.0f}")
            st.success(f"📌 FCF per Share: ${data['fcf_per_share']:.2f}")
            st.success(f"💰 Caesar's Value: ${data['dcf_per_share']:.2f}")
        else:
            st.error(f"❌ Error: {res.status_code} - {res.text}")
    except Exception as e:
        st.error(f"❌ Request failed: {e}")
