import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Futuristic clean bubble style with light background
st.set_page_config(page_title="Caesar's Quick Value Finder", layout="centered")
st.markdown("""
    <style>
    body {
        background-color: #f7f9fb;
        color: #1a1a1a;
        font-family: 'Segoe UI', sans-serif;
    }
    .stApp {
        background: linear-gradient(to bottom, #f7f9fb, #e6eef5);
    }
    .css-1cpxqw2, .css-ffhzg2, .css-1v3fvcr {
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        background: #ffffff;
        border: 1px solid #dfe6ec;
        padding: 1.5em;
    }
    .stButton > button {
        background-color: #13c2c2;
        color: white;
        border-radius: 30px;
        padding: 0.6em 1.2em;
        font-weight: bold;
        border: none;
    }
    .stTextInput > div > input, .stNumberInput > div > input {
        background-color: #ffffff;
        color: #1a1a1a;
        border-radius: 10px;
        border: 1px solid #d0d7de;
        padding: 0.5em;
    }
    </style>
""", unsafe_allow_html=True)

# Title and inputs
st.title("🛡️ Caesar's Quick Value Finder")
ticker = st.text_input("🔍 Enter Stock Ticker (e.g. AAPL)", value="AAPL")
user_cagr = st.number_input("📈 Enter FCF Growth Rate (%)", min_value=0.0, max_value=50.0, value=5.0)

# Constants
DISCOUNT_RATE = 0.06
TERMINAL_MULTIPLE = 10

# Fetch data
if st.button("🚀 Calculate Valuation"):
    try:
        ticker_obj = yf.Ticker(ticker)
        financials = ticker_obj.financials.T
        cashflow = ticker_obj.cashflow.T
        info = ticker_obj.info

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

            shares_keys = ["Diluted Average Shares", "Basic Average Shares"]
            shares_out = find_value(financials, shares_keys)
            if shares_out is None or shares_out == 0:
                raise ValueError("Could not determine share count.")

            fcf_per_share = fcf / shares_out

            # DCF Calculation
            cagr = user_cagr / 100
            years = 10  # 10-year DCF
            projected_fcf = [fcf * ((1 + cagr) ** i) for i in range(1, years + 1)]
            terminal_value = projected_fcf[-1] * TERMINAL_MULTIPLE
            cashflows = projected_fcf + [terminal_value]

            discounted = [cf / ((1 + DISCOUNT_RATE) ** (i + 1)) for i, cf in enumerate(cashflows)]
            dcf_value = sum(discounted)
            dcf_per_share = dcf_value / shares_out

            # Output
            st.success(f"✅ FCF: ${fcf:,.0f}")
            st.success(f"📌 FCF per Share: ${fcf_per_share:.2f}")
            st.success(f"🏛️ Caesar's Value: ${dcf_per_share:.2f}")

            # Graph
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=[f"Year {i+1}" for i in range(years)],
                y=projected_fcf,
                mode='lines+markers',
                name="Projected FCF",
                line=dict(color='#005073')
            ))
            fig.update_layout(
                title="📈 Projected Free Cash Flow",
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
                font_color="#1a1a1a"
            )
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.error("❌ Could not find all required data (Net Income, Depreciation, or CapEx).")

    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
