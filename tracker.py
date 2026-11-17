import yfinance as yf

# NSE stocks use the .NS suffix (e.g. RELIANCE.NS, TCS.NS, INFY.NS)
ticker = "TCS.NS"

data = yf.download(ticker, period="6mo", auto_adjust=True)
data.columns = data.columns.get_level_values(0)  # flatten the extra column level
print(data.tail())

latest_close = float(data["Close"].iloc[-1])
print(f"\nLatest closing price of {ticker}: ₹{latest_close:.2f}")

# New lines added at the end
print(f"Highest close: ₹{data['Close'].max():.2f}")
print(f"Lowest close: ₹{data['Close'].min():.2f}")
print(f"Money traded today: ₹{data['Close'].iloc[-1] * data['Volume'].iloc[-1]:,.0f}")