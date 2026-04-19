# 📊 Stock Analyzer Agent

A Python-based stock analysis tool that fetches real-time stock data and generates insights using an AI model.

## 🚀 Features
- Fetch stock data using Yahoo Finance
- Analyze price trend (Uptrend / Downtrend)
- AI-generated insights (Grok API)
- Fallback logic if API fails

## 🛠️ Tech Stack
- Python
- yfinance
- requests
- dotenv

## ▶️ How to Run

pip install -r requirements.txt  
python stock_agent.py  

## 🌐 Example

Input: TCS.NS  
Output: Price + Trend + AI Insight  

## ⚠️ Note
If AI API fails, fallback logic ensures system still works.

## 📌 Future Improvements
- Add Streamlit UI  
- Add charts  
- Add sentiment analysis  