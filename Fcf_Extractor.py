import streamlit as st
from sec_edgar_downloader import Downloader
import os, re

def extract_fcf(ticker):
    # Download 10-K
    dl = Downloader("sec_data")
    dl.get("10-K", ticker, amount=1)

    # Locate filing
    filing_dir = f"sec_data/sec-edgar-filings/{ticker}/10-K"
    latest_filing = sorted(os.listdir(filing_dir))[-1]
    file_path = os.path.join(filing_dir, latest_filing, "full-submission.txt")
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    # Helper
    def find(pattern):
        match = re.search(pattern, text, re.IGNORECASE)
        return float(match.group(1).replace(",", "")) if match else None

    net_income = find(r"net (income|earnings).*?\$?([\d,]+\.?\d*)")
    d_and_a = find(r"depreciation and amortization.*?\$?([\d,]+\.?\d*)")
    capex = find(r"(capital expenditures|purchases of property and equipment).*?\$?([\d,]+\.?\d*)")

    if net_income is not None and d_and_a is not None and capex is not None:
        fcf = net_income + d_and_a - capex
    else:
        fcf = None

    return net_income, d_and_a, capex, fcf

# Streamlit UI
st.title("FCF Calculator from 10-K")

ticker = st.text_input("Enter stock ticker:", "AAPL")

if st.button("Calculate FCF"):
    try:
        net_income, d_and_a, capex, fcf = extract_fcf(ticker.upper())
        st.write(f"**Net Income:** ${net_income:,.0f}" if net_income else "Net Income not found")
        st.write(f"**Depreciation & Amortization:** ${d_and_a:,.0f}" if d_and_a else "D&A not found")
        st.write(f"**Capital Expenditures:** ${capex:,.0f}" if capex else "CapEx not found")

        if fcf is not None:
            st.markdown(f"### ✅ Free Cash Flow (FCF): ${fcf:,.0f}")
        else:
            st.error("Could not calculate FCF. Some values are missing.")
    except Exception as e:
        st.error(f"Error: {str(e)}")
