import yfinance as yf
import matplotlib.pyplot as plt

# NSE stocks use the .NS suffix (e.g. RELIANCE.NS, TCS.NS, INFY.NS)
ticker = "RELIANCE.NS"

data = yf.download(ticker, period="6mo", auto_adjust=True)
data.columns = data.columns.get_level_values(0)  # flatten the extra column level

plt.figure(figsize=(10, 5))
plt.plot(data.index, data["Close"], label="Close price")
plt.title(f"{ticker} - Last 6 Months")
plt.xlabel("Date")
plt.ylabel("Price (₹)")
plt.legend()
plt.grid(True)
plt.show()