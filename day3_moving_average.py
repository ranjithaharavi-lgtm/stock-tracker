import yfinance as yf
import matplotlib.pyplot as plt

ticker = "RELIANCE.NS"

data = yf.download(ticker, period="1y", auto_adjust=True)
data.columns = data.columns.get_level_values(0)

data["MA20"] = data["Close"].rolling(window=20).mean()
data["MA50"] = data["Close"].rolling(window=50).mean()

plt.figure(figsize=(10, 5))
plt.plot(data.index, data["Close"], label="Close", alpha=0.6)
plt.plot(data.index, data["MA20"], label="20-day average")
plt.plot(data.index, data["MA50"], label="50-day average")
plt.title(f"{ticker} - Price with Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price (₹)")
plt.legend()
plt.grid(True)
plt.show()