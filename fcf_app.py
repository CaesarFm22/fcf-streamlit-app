import streamlit as st
import yfinance as yf
import pandas as pd

def find_row(df, keywords):
    for row in df.index:
        if any(kw.lower() in row.lower() for kw in keywords):
            value = df.loc[row].iloc[0]
            st.write(f"✅ Found '{row}': {value}")
            return value
    st.write(f"❌ No match found for: {keywords}")
    return None

st.title("📊 Free Cash Flow (FCF) Calculator")

ticker = st.text_input("Enter stock ticker (e.g., AAPL, MSFT):")

if st.button("Calculate FCF") and ticker:
    try:
        stock = yf.Ticker(ticker)
        financials = stock.financials
        cashflow = stock.cashflow

        # Debug: Show full raw financials and cashflow tables
        st.subheader("Raw Financials:")
        st.dataframe(financials)

        st.subheader("Raw Cash Flow:")
        st.dataframe(cashflow)

        # Print available row names
        st.write("🔍 Cash Flow Row Index:")
        st.write(list(cashflow.index))

        # Extract components
        net_income = find_row(financials, ["net income"])
        depreciation = find_row(cashflow, [
            "depreciation amortization",
            "depreciation",
            "amortization"
        ])
        capex = find_row(cashflow, [
            "capital expenditures",
            "capital expenditure",
            "capital expenditures payments",
            "purchase of property plant",
            "purchase of fixed assets"
        ])

        # Validate all data is present
        if any(x is None or pd.isna(x) for x in [net_income, depreciation, capex]):
            st.error("❌ Could not find all required data (Net Income, Depreciation, or CapEx).")
        else:
            fcf = net_income + depreciation - capex
            st.metric("Net Income", f"${net_income:,.0f}")
            st.metric("Depreciation & Amortization", f"${depreciation:,.0f}")
            st.metric("CapEx", f"${capex:,.0f}")
            st.metric("📈 Free Cash Flow", f"${fcf:,.0f}")

            # Add FCF per Share
            shares_outstanding = stock.info.get("sharesOutstanding")
            if shares_outstanding:
                fcf_per_share = fcf / shares_outstanding
                st.metric("🧮 Shares Outstanding", f"{shares_outstanding:,.0f}")
                st.metric("💵 FCF per Share", f"${fcf_per_share:.2f}")
            else:
                st.warning("⚠️ Shares Outstanding not available.")


    except Exception as e:
        st.error(f"❌ Error: {e}")
