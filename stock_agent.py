import yfinance as yf
import requests
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()


# -------------------------------
# Step 1: Get stock data
# -------------------------------
def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="5d")
    return data


# -------------------------------
# Step 2: Analyze stock
# -------------------------------
def analyze_stock(data):
    first_price = data['Close'].iloc[0]
    last_price = data['Close'].iloc[-1]

    if last_price > first_price:
        trend = "Uptrend 📈"
    else:
        trend = "Downtrend 📉"

    return round(last_price, 2), trend


# -------------------------------
# Step 3: Grok API (SAFE VERSION)
# -------------------------------
def explain_with_grok(price, trend, symbol):
    api_key = os.getenv("GROK_API_KEY")

    if not api_key:
        return "⚠️ API key missing"

    url = "https://api.x.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    Stock: {symbol}
    Current Price: {price}
    Trend: {trend}

    Explain in simple terms if this is a good or bad sign.
    """

    payload = {
        "model": "grok-2-latest",   # safer model
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload)

        # DEBUG (you can remove later)
        print("DEBUG RESPONSE:", response.text)

        if response.status_code != 200:
            return f"⚠️ Grok API Error ({response.status_code})"

        result = response.json()

        # Safe extraction
        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            return "⚠️ No response from AI"

    except Exception as e:
        return f"⚠️ API failed: {str(e)}"


# -------------------------------
# Step 4: Agent
# -------------------------------
def stock_agent(symbol):
    data = get_stock_data(symbol)

    if data.empty:
        return "❌ Invalid stock symbol"

    price, trend = analyze_stock(data)

    explanation = explain_with_grok(price, trend, symbol)

    # 🔥 FALLBACK (IMPORTANT)
    if "⚠️" in explanation:
        explanation = f"The stock is showing a {trend} based on recent price movement."

    return f"""
📊 Stock: {symbol}
💰 Price: {price}
📈 Trend: {trend}

🧠 AI Insight:
{explanation}
"""


# -------------------------------
# Step 5: Run
# -------------------------------
if __name__ == "__main__":
    symbol = input("Enter stock symbol (e.g., AAPL, TCS.NS): ")

    result = stock_agent(symbol)

    print(result)