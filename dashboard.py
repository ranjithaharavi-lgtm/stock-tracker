import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stock Tracker", layout="wide")
st.title("Stock Tracker Dashboard")

# Sidebar inputs
ticker = st.sidebar.text_input("Ticker (NSE stocks end with .NS)", "RELIANCE.NS")
period = st.sidebar.selectbox("Period", ["6mo", "1y", "2y", "5y"], index=2)
short_w = st.sidebar.number_input("Short average (days)", 5, 50, 20)
long_w = st.sidebar.number_input("Long average (days)", 20, 200, 50)


@st.cache_data
def load_data(ticker, period):
    df = yf.download(ticker, period=period, auto_adjust=True)
    if df.empty:
        return df
    df.columns = df.columns.get_level_values(0)
    return df


data = load_data(ticker, period)

if data.empty:
    st.error("No data found. Check the ticker (for example RELIANCE.NS).")
    st.stop()

# Summary numbers
latest = float(data["Close"].iloc[-1])
col1, col2, col3 = st.columns(3)
col1.metric("Latest close", f"₹{latest:.2f}")
col2.metric("Highest close", f"₹{data['Close'].max():.2f}")
col3.metric("Lowest close", f"₹{data['Close'].min():.2f}")

# Moving averages chart
data["MA_short"] = data["Close"].rolling(short_w).mean()
data["MA_long"] = data["Close"].rolling(long_w).mean()

st.subheader("Price with moving averages")
fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(data.index, data["Close"], label="Close", alpha=0.6)
ax1.plot(data.index, data["MA_short"], label=f"{short_w}-day average")
ax1.plot(data.index, data["MA_long"], label=f"{long_w}-day average")
ax1.set_ylabel("Price (₹)")
ax1.legend()
ax1.grid(True)
fig1.autofmt_xdate()
st.pyplot(fig1)

# Backtest
bt = data.copy()
bt["Signal"] = (bt["MA_short"] > bt["MA_long"]).astype(int)
bt["Position"] = bt["Signal"].shift(1)
bt = bt.dropna()

if len(bt) < 2:
    st.warning("Not enough data for the backtest. Choose a longer period.")
    st.stop()

bt["Daily_Return"] = bt["Close"].pct_change().fillna(0)
bt["Strategy_Return"] = bt["Daily_Return"] * bt["Position"]
bt["Buy_Hold"] = (1 + bt["Daily_Return"]).cumprod()
bt["Strategy"] = (1 + bt["Strategy_Return"]).cumprod()

bh_ret = (bt["Buy_Hold"].iloc[-1] - 1) * 100
st_ret = (bt["Strategy"].iloc[-1] - 1) * 100
actions = int(bt["Position"].diff().abs().sum())

st.subheader("Backtest: crossover strategy vs buy and hold")
c1, c2, c3 = st.columns(3)
c1.metric("Buy and hold", f"{bh_ret:.2f}%")
c2.metric("Strategy", f"{st_ret:.2f}%")
c3.metric("Buy/sell actions", actions)

fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.plot(bt.index, bt["Buy_Hold"], label="Buy and hold")
ax2.plot(bt.index, bt["Strategy"], label="Crossover strategy")
ax2.set_ylabel("Growth of ₹1")
ax2.legend()
ax2.grid(True)
fig2.autofmt_xdate()
st.pyplot(fig2)

st.caption("Educational only. Ignores brokerage, taxes and slippage. Past results do not predict the future.")