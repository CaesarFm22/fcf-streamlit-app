import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Set dark-friendly background color
st.markdown("""
    <style>
        body, .stApp {
            background-color: #1e1e1e;
        }
        label, .stTextInput>div>input, .stNumberInput>div>input, .stNumberInput label, .stTextInput label, .stMarkdown {
            color: white !important;
        }
        .stTable tbody tr td {
            background-color: white !important;
            color: black !important;
        }
        .stTable thead tr th {
            background-color: white !important;
            color: black !important;
        }
        .stTitle h1, .stTitle h2, .stTitle h3 {
            color: white !important;
        }
        h1 {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Display logo and YouTube icon with link
st.markdown("""
<div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
    <a href="https://www.youtube.com/@CaesarFM-h9z" target="_blank" style="display: flex; align-items: center; gap: 12px;">
        <img src="https://github.com/CaesarFm22/fcf-app2.0/blob/main/ChatGPT%20Image%20Jul%2010,%202025,%2006_34_37%20PM.png?raw=true" width="100" alt="Logo">
        <img src="https://upload.wikimedia.org/wikipedia/commons/e/ef/Youtube_logo.png" width="60" alt="YouTube">
    </a>
</div>
""", unsafe_allow_html=True)

# App input and layout
st.title("Caesar's Stock Valuation App")
ticker = st.text_input("Enter Stock Ticker (e.g. AAPL, MSFT):", "AAPL")
cagr_input = st.number_input("Expected CAGR (%):", min_value=0.0, max_value=50.0, value=10.0)

if ticker:
    stock = yf.Ticker(ticker)
    info = stock.info
    cashflow = stock.cashflow
    financials = stock.financials
    balance_sheet = stock.balance_sheet

    try:
        # Extract key values
        net_income = financials.loc["Net Income"].iloc[0]

        capex = 0
        for label in ["Capital Expenditures", "CapitalExpenditures"]:
            if label in cashflow.index:
                capex = cashflow.loc[label].iloc[0]
                break

        ddna = 0
        for label in ["Depreciation", "Depreciation & Amortization", "Depreciation And Amortization"]:
            if label in financials.index:
                ddna = financials.loc[label].iloc[0]
                break

        shares_outstanding = info.get("sharesOutstanding", 0)
        price = info.get("currentPrice", 0)
        dividends_per_share = info.get("dividendRate", 0)
        treasury = balance_sheet.loc["Treasury Stock"].iloc[0] if "Treasury Stock" in balance_sheet.index else 0
        market_cap = price * shares_outstanding
        book_value = info.get("bookValue", 0)

        # Ratios
        roa = info.get("returnOnAssets", 0)
        roe = info.get("returnOnEquity", 0)
        current_ratio = info.get("currentRatio", 0)
        quick_ratio = info.get("quickRatio", 0)

        total_cash = balance_sheet.loc["Cash"].iloc[0] if "Cash" in balance_sheet.index else 0
        total_debt = balance_sheet.loc["Total Debt"].iloc[0] if "Total Debt" in balance_sheet.index else 0
        total_equity = balance_sheet.loc["Total Stockholder Equity"].iloc[0] if "Total Stockholder Equity" in balance_sheet.index else 0

        cash_to_debt = total_cash / total_debt if total_debt != 0 else 0
        debt_to_equity = total_debt / total_equity if total_equity != 0 else 0

        sgr = roe * (1 - (dividends_per_share / (net_income / shares_outstanding))) if shares_outstanding != 0 else 0

        # Corrected FCF / Owner Earnings logic using Net Income instead of Operating Cash Flow
        adjusted_cost = ddna if abs(ddna) > abs(capex) else capex
        fcf = net_income - adjusted_cost

        cagr = cagr_input / 100
        intrinsic_value = fcf * (1 + cagr)**10
        caesar_value = intrinsic_value / shares_outstanding

        # Determine valuation
        margin = 0.10 * caesar_value
        if price > caesar_value + margin:
            valuation_label = "overvalued"
            valuation_color = "red"
        elif price < caesar_value - margin:
            valuation_label = "undervalued"
            valuation_color = "green"
        else:
            valuation_label = "fairly valued"
            valuation_color = "yellow"

        # Build the metric list manually
        metrics = pd.DataFrame({
            "Metric": [
                "Price",
                "Market Cap",
                "Caesar's Value",
                "Caesar's Value/Share",
                "Market Share",
                "Margin of Safety",
                "Dividends/share",
                "Treasury",
                "Book Value",
                "ROA",
                "ROE",
                "Current Ratio",
                "Quick Ratio",
                "Cash to Debt",
                "Debt to Equity",
                "SGR"
            ]
        })

        st.table(metrics)

        # Display Caesar's conclusion
        st.markdown(f"""
        <h3 style='text-align: center; color: black;'>According to Caesar, this stock is 
            <span style='color: {valuation_color};'>{valuation_label}</span>.</h3>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
