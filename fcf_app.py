import streamlit as st
import yfinance as yf
import pandas as pd

# Debug toggle
DEBUG = False  # Set to True to show all available financial keys

# Title and inputs
st.title("📊 FCF & DCF Valuation App")
ticker = st.text_input("Enter Stock Ticker (e.g. AAPL)", value="AAPL")
user_cagr = st.number_input("Enter FCF Growth Rate (%)", min_value=0.0, max_value=50.0, value=5.0)

# Constants
DISCOUNT_RATE = 0.06
TERMINAL_MULTIPLE = 10

# Fetch data
if st.button("Calculate"):
    try:
        ticker_obj = yf.Ticker(ticker)
        financials = ticker_obj.financials.T
        cashflow = ticker_obj.cashflow.T
        info = ticker_obj.info

        if DEBUG:
            st.write("🔎 Available Financials:")
            st.write(list(financials.columns))
            st.write("🔎 Available Cashflow:")
            st.write(list(cashflow.columns))

        # Try common field names
        net_income_keys = ["Net Income", "Net Income Common Stockholders", "Net Income Including Noncontrolling Interests"]
        depreciation_keys = ["Depreciation Amortization Depletion", "Depreciation And Amortization"]
        capex_keys = ["Capital Expenditure", "Capital Expenditure Reported"]

        def find_value(df, keys):
            for key in keys:
                if key in df.columns:
                    return df[key].iloc[0]
            return None

        net_income = find_value(financials, net_income_keys)
        depreciation = find_value(cashflow, depreciation_keys)
        capex = find_value(cashflow, capex_keys)

        if all(v is not None for v in [net_income, depreciation, capex]):
            fcf = net_income + depreciation - capex

            # Get shares outstanding
            shares_keys = ["Diluted Average Shares", "Basic Average Shares"]
            shares_out = find_value(financials, shares_keys)
            if shares_out is None or shares_out == 0:
                raise ValueError("Could not determine share count.")

            fcf_per_share = fcf / shares_out

            # DCF Calculation
            cagr = user_cagr / 100
            years = 5
            projected_fcf = [fcf * ((1 + cagr) ** i) for i in range(1, years + 1)]
            terminal_value = projected_fcf[-1] * TERMINAL_MULTIPLE
            cashflows = projected_fcf + [terminal_value]

            discounted = [
                cf / ((1 + DISCOUNT_RATE) ** (i + 1)) for i, cf in enumerate(cashflows)
            ]
            dcf_value = sum(discounted)
            dcf_per_share = dcf_value / shares_out

            # Output
            st.success(f"✅ FCF: ${fcf:,.0f}")
            st.success(f"📌 FCF per Share: ${fcf_per_share:.2f}")
            st.success(f"📈 DCF Valuation per Share: ${dcf_per_share:.2f}")

            # CAGR Placeholder (implement with historical FCF if needed)
            st.markdown("### 📊 Historical CAGR (Coming Soon)")
            st.markdown("- 5-year FCF CAGR: 🔧 To implement")
            st.markdown("- 10-year FCF CAGR: 🔧 To implement")
            st.markdown("- 20-year FCF CAGR: 🔧 To implement")

        else:
            st.error("❌ Could not find all required data (Net Income, Depreciation, or CapEx).")

    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
