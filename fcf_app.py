import streamlit as st
import yfinance as yf
import pandas as pd

st.title("📊 Free Cash Flow (FCF) Calculator")

ticker = st.text_input("Enter stock ticker (e.g., AAPL):")
user_cagr = st.number_input("Enter FCF CAGR (%)", min_value=0.0, max_value=50.0, value=5.0)
calculate = st.button("Calculate FCF")

def safe_lookup(df, keys):
    for key in keys:
        matches = df[df.index.str.lower() == key.lower()]
        if not matches.empty:
            return matches.iloc[0, 0]
        matches = df[df.index.str.lower().str.contains(key.lower())]
        if not matches.empty:
            return matches.iloc[0, 0]
    return None

if calculate and ticker:
    try:
        stock = yf.Ticker(ticker)
        financials = stock.financials
        cashflow = stock.cashflow
        shares = stock.info.get("sharesOutstanding", None)

        st.write("🔎 Available Financials:", list(financials.index))
        st.write("🔎 Available Cashflow:", list(cashflow.index))

        ni_keys = [
            "Net Income",
            "Net Income From Continuing Operations",
            "Net Income Common Stockholders"
        ]
        dep_keys = [
            "Depreciation Amortization Depletion",
            "Depreciation And Amortization"
        ]
        capex_keys = ["Capital Expenditure"]

        ni = safe_lookup(financials, ni_keys)
        d_and_a = safe_lookup(cashflow, dep_keys)
        capex = safe_lookup(cashflow, capex_keys)

        if ni is not None and d_and_a is not None and capex is not None:
            fcf = ni + d_and_a - capex
            st.success(f"✅ FCF: ${fcf:,.0f}")

            if shares:
                fcf_per_share = fcf / shares
                st.info(f"📌 FCF per Share: ${fcf_per_share:.2f}")

                # DCF Valuation
                discount_rate = 0.06
                cagr = user_cagr / 100
                years = 5
                fcf_list = [fcf * ((1 + cagr) ** i) for i in range(1, years + 1)]
                terminal_value = fcf_list[-1] * 10
                discounted_cashflows = [fcf_list[i] / ((1 + discount_rate) ** (i + 1)) for i in range(years)]
                discounted_terminal = terminal_value / ((1 + discount_rate) ** years)
                total_dcf = sum(discounted_cashflows) + discounted_terminal

                if shares:
                    dcf_per_share = total_dcf / shares
                    st.success(f"📈 DCF Valuation per Share: ${dcf_per_share:.2f}")
            else:
                st.warning("⚠️ Could not find shares outstanding.")
        else:
            st.error("❌ Could not find all required data (Net Income, Depreciation, or CapEx).")

    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
