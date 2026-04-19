from flask import Flask, render_template, request, jsonify
import yfinance as yf
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Stock analysis functions
def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="5d")
        return data
    except Exception as e:
        return None


def analyze_stock(data):
    try:
        first_price = data['Close'].iloc[0]
        last_price = data['Close'].iloc[-1]

        if last_price > first_price:
            trend = "uptrend"
        else:
            trend = "downtrend"

        return round(last_price, 2), trend
    except Exception as e:
        return None, None


def explain_with_grok(price, trend, symbol):
    api_key = os.getenv("GROK_API_KEY")

    if not api_key:
        return "Error: GROK_API_KEY not found in environment variables"

    url = "https://api.x.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    Analyze this stock:
    Symbol: {symbol}
    Current Price: {price}
    Trend: {trend}

    Explain in simple terms if it's a good sign or not.
    """

    payload = {
        "model": "grok-beta",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        result = response.json()

        if "error" in result:
            error = result['error']
            if isinstance(error, dict):
                error_msg = error.get('message', 'Unknown error')
            else:
                error_msg = str(error)
            return f"API Error: {error_msg}"
        
        if "choices" not in result:
            return f"Unexpected API response: {result}"

        return result["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        return "Error: API request timed out"
    except Exception as e:
        return f"Error: {str(e)}"


# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        symbol = data.get('symbol', '').strip().upper()

        if not symbol:
            return jsonify({"error": "Please enter a stock symbol"}), 400

        # Get stock data
        stock_data = get_stock_data(symbol)

        if stock_data is None or stock_data.empty:
            return jsonify({"error": f"Invalid stock symbol: {symbol}"}), 400

        # Analyze stock
        price, trend = analyze_stock(stock_data)

        if price is None:
            return jsonify({"error": "Error analyzing stock data"}), 500

        # Get AI explanation
        explanation = explain_with_grok(price, trend, symbol)

        return jsonify({
            "symbol": symbol,
            "price": price,
            "trend": trend,
            "explanation": explanation
        })

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
