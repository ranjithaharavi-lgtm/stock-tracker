import yfinance as yf
import matplotlib.pyplot as plt

ticker = "INFY.NS"

data = yf.download(ticker, period="2y", auto_adjust=True)
data.columns = data.columns.get_level_values(0)

data["MA20"] = data["Close"].rolling(20).mean()
data["MA50"] = data["Close"].rolling(50).mean()

# 1 = holding the stock, 0 = sitting in cash
data["Signal"] = (data["MA20"] > data["MA50"]).astype(int)

# Trade on yesterday's signal, so we never use future information
data["Position"] = data["Signal"].shift(1)

data = data.dropna()

data["Daily_Return"] = data["Close"].pct_change()
data["Strategy_Return"] = data["Daily_Return"] * data["Position"]

# Growth of ₹1 invested
data["Buy_Hold"] = (1 + data["Daily_Return"].fillna(0)).cumprod()
data["Strategy"] = (1 + data["Strategy_Return"].fillna(0)).cumprod()

buy_hold = (data["Buy_Hold"].iloc[-1] - 1) * 100
strategy = (data["Strategy"].iloc[-1] - 1) * 100
trades = int(data["Position"].diff().abs().sum())

print(f"Buy and hold return: {buy_hold:.2f}%")
print(f"Strategy return:     {strategy:.2f}%")
print(f"Number of buy/sell actions: {trades}")

plt.figure(figsize=(10, 5))
plt.plot(data.index, data["Buy_Hold"], label="Buy and hold")
plt.plot(data.index, data["Strategy"], label="MA crossover strategy")
plt.title(f"{ticker} - Strategy vs Buy and Hold")
plt.xlabel("Date")
plt.ylabel("Growth of ₹1")
plt.legend()
plt.grid(True)
plt.show()
