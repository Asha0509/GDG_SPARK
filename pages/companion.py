import streamlit as st
import yfinance as yf
import requests
import pandas as pd

st.set_page_config(page_title="SaaS Investing Companion", layout="wide")
st.title("💼 S.P.A.R.K Investing Companion (GDG Hackathon Safe)")

# ✅ Your official EODHD API Key here:
EODHD_API_KEY = "67d6ebbd2ee232.15990921"

# User inputs
amount = st.number_input("💰 Amount to Invest (INR)", min_value=1000, max_value=2000000, step=500)
risk = st.radio("🧩 Risk Profile", ["Low Risk (<= ₹5k)", "Medium Risk (<= ₹30k)"])
sector_pref = st.selectbox("🏦 Preferred Sector", ["Any", "Financial Services", "Technology", "Consumer Defensive", "Healthcare"])

st.markdown("---")

### STEP 1️⃣: yfinance to fetch top NSE stocks
nse_symbols = [
    "RELIANCE.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", "TCS.NS",
    "ITC.NS", "LT.NS", "SBIN.NS", "BHARTIARTL.NS", "KOTAKBANK.NS", "WIPRO.NS"
]

def display_risk(beta):
    if beta is None:
        return "⚪ Unknown"
    if beta < 0.9:
        return "🟢 Low Volatility"
    elif 0.9 <= beta <= 1.2:
        return "🟡 Medium Volatility"
    else:
        return "🔴 High Volatility"

### STEP 2️⃣: EODHD - Historical Chart
def get_eodhd_chart(symbol):
    url = f"https://eodhistoricaldata.com/api/eod/{symbol}.NS?api_token={EODHD_API_KEY}&fmt=json&period=6mo"
    response = requests.get(url)
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        return df
    else:
        return pd.DataFrame()

### STEP 3️⃣: Recommendation Engine
def recommend_stocks():
    with st.spinner("🔄 Fetching your personalized recommendations..."):
        shortlisted = []

        for ticker in nse_symbols:
            stock = yf.Ticker(ticker)
            info = stock.info

            if info.get('marketCap') is None or info.get('beta') is None:
                continue

            stock_sector = info.get('sector', 'N/A')
            if sector_pref != "Any" and stock_sector != sector_pref:
                continue

            if risk.startswith("Low") and info.get('beta') >= 0.9:
                continue
            if risk.startswith("Medium") and info.get('beta') < 0.9:
                continue

            shortlisted.append(info)
            if len(shortlisted) >= 5:
                break

        if not shortlisted:
            st.warning("❌ No matching stocks found for your risk/sector profile.")
            return

        for stock_info in shortlisted:
            symbol = stock_info['symbol']
            beta = stock_info.get('beta', None)
            risk_score = display_risk(beta)

            st.markdown(f"### **{stock_info.get('shortName', symbol)} ({symbol})**")
            st.write(f"• Sector: {stock_info.get('sector', 'N/A')}")
            st.write(f"• Current Price: ₹{stock_info['regularMarketPrice']}")
            st.write(f"• Beta: {round(beta, 2) if beta else 'N/A'} ({risk_score})")
            st.write(f"• Dividend Yield: {round(stock_info.get('dividendYield', 0) * 100, 2) if stock_info.get('dividendYield') else 'N/A'}%")
            st.write(f"• Market Cap: ₹{round(stock_info['marketCap'] / 1e9, 2)} B INR")

            eodhd_df = get_eodhd_chart(symbol.replace(".NS", ""))
            if not eodhd_df.empty:
                st.line_chart(eodhd_df['close'])
            else:
                st.warning("⚠️ Chart unavailable via EODHD API.")
            st.write("---")

if st.button("📊 Show My Recommended Stocks"):
    recommend_stocks()

### Glossary
st.markdown("""
### 🧠 **Glossary**
- **Beta:** Risk score (volatility)
- **Low Beta (<0.9):** Lower risk  
- **High Beta (>1.2):** More volatile  
- **Dividend Yield:** % returned yearly to investors  
- **EOD:** End-of-day price data (from EODHD API)
""", unsafe_allow_html=True)
