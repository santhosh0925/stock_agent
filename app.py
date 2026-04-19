import streamlit as st
from stock_agent import stock_agent

st.title("📊 Stock Analyzer Agent")

STOCK_GROUPS = {
    "US Stocks": [
        ("AAPL", "Apple"),
        ("GOOGL", "Google"),
        ("MSFT", "Microsoft"),
        ("AMZN", "Amazon"),
        ("TSLA", "Tesla"),
        ("META", "Meta"),
        ("NVDA", "NVIDIA"),
        ("BRK.B", "Berkshire Hathaway"),
        ("JNJ", "Johnson & Johnson"),
        ("V", "Visa"),
    ],
    "Indian Stocks": [
        ("TCS.NS", "Tata Consultancy"),
        ("INFY.NS", "Infosys"),
        ("RELIANCE.NS", "Reliance"),
        ("HDFCBANK.NS", "HDFC Bank"),
        ("WIPRO.NS", "Wipro"),
        ("ICICIBANK.NS", "ICICI Bank"),
        ("LT.NS", "Larsen & Toubro"),
        ("BAJAJ-AUTO.NS", "Bajaj Auto"),
    ],
    "Other Popular": [
        ("BZ=F", "Brent Crude Oil"),
        ("GC=F", "Gold Futures"),
        ("EURUSD=X", "EUR/USD"),
    ],
}

CUSTOM_SYMBOL = "Custom symbol..."

_stock_display = {}
_stock_symbols = []
for group_name, group_items in STOCK_GROUPS.items():
    for sym, name in group_items:
        _stock_symbols.append(sym)
        _stock_display[sym] = f"{name} ({sym}) — {group_name}"

selected = st.selectbox(
    "Select Stock",
    options=[CUSTOM_SYMBOL] + _stock_symbols,
    format_func=lambda s: s if s == CUSTOM_SYMBOL else _stock_display.get(s, s),
)

if selected == CUSTOM_SYMBOL:
    symbol = st.text_input("Enter Stock Symbol (AAPL, TCS.NS):", placeholder="AAPL")
else:
    symbol = selected

if st.button("Analyze"):
    if symbol:
        result = stock_agent(symbol)
        st.text(result)
    else:
        st.warning("Please enter a stock symbol")
