import os
import requests
import yfinance as yf
from dotenv import load_dotenv

# Load environment variables from .env file in the project root
load_dotenv()

# -------------------------------
# Step 1: Get stock data
# -------------------------------
def get_stock_data(symbol):
    """Fetch the last 5 days of stock history for the requested symbol."""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="5d")

        if data.empty:
            return None

        return data
    except Exception:
        return None


# -------------------------------
# Step 2: Basic analysis
# -------------------------------
def analyze_stock(data):
    """Compare the first and last closing prices to determine the trend."""
    if data is None or data.empty:
        return None, None

    first_close = data["Close"].iloc[0]
    last_close = data["Close"].iloc[-1]
    trend = "Uptrend" if last_close > first_close else "Downtrend"

    return round(last_close, 2), trend


# -------------------------------
# Step 3: Grok API call
# -------------------------------
def explain_with_grok(price, trend, symbol):
    """Send the stock price and trend to Grok and return a readable explanation."""
    api_key = os.getenv("GROK_API_KEY")
    if not api_key:
        return "Error: GROK_API_KEY is missing from environment variables."

    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    prompt = (
        f"Analyze this stock:\n"
        f"Symbol: {symbol}\n"
        f"Current Price: {price}\n"
        f"Trend: {trend}\n\n"
        "Explain in simple terms if it's a good sign or not."
    )

    payload = {
        "model": "grok-beta",
        "messages": [
            {"role": "user", "content": prompt}
        ],
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.RequestException as exc:
        return f"Error: API request failed ({exc})"
    except ValueError:
        return "Error: Unable to parse API response as JSON."

    if "choices" not in result or not isinstance(result["choices"], list) or len(result["choices"]) == 0:
        if "error" in result:
            error = result["error"]
            if isinstance(error, dict):
                return f"Error: {error.get('message', 'Unknown API error')}"
            return f"Error: {error}"
        return f"Error: Unexpected API response structure: {result}"

    choice = result["choices"][0]
    message = choice.get("message", {}) if isinstance(choice, dict) else {}
    content = message.get("content") if isinstance(message, dict) else None

    if not content:
        return f"Error: Missing text content in Grok response: {result}"

    return content.strip()


# -------------------------------
# Step 4: Agent
# -------------------------------
def stock_agent(symbol):
    """Run the stock analyzer agent workflow for the given symbol."""
    symbol = symbol.strip()
    if not symbol:
        return None, None, "Error: Stock symbol cannot be empty."

    data = get_stock_data(symbol)
    if data is None or data.empty:
        return None, None, f"Error: Invalid stock symbol or no data available for '{symbol}'."

    price, trend = analyze_stock(data)
    if price is None:
        return None, None, f"Error: Unable to analyze stock data for '{symbol}'."

    explanation = explain_with_grok(price, trend, symbol)
    return price, trend, explanation


# -------------------------------
# Step 5: Run
# -------------------------------
if __name__ == "__main__":
    user_symbol = input("Enter stock symbol (for example AAPL or TCS.NS): ")
    price, trend, explanation = stock_agent(user_symbol)

    if price is None or trend is None:
        print(explanation)
    else:
        print(f"Stock: {user_symbol}")
        print(f"Price: {price}")
        print(f"Trend: {trend}")
        print(f"AI Insight: {explanation}")
