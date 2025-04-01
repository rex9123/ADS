import streamlit as st
import yfinance as yf
import requests
import google.generativeai as genai
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from textblob import TextBlob

# Configure Gemini API Key (Replace with actual key)
GEMINI_API_KEY = "AIzaSyBlTtwu9XObXiWynLSRWlZGVU4jEkhm0H8"
genai.configure(api_key=GEMINI_API_KEY)

def fetch_market_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="5d")
    if hist.empty:
        return "Invalid ticker or no data available."
    return hist

def generate_ai_insights(ticker, market_data):
    prompt = f"Analyze the past 5 days' closing prices for {ticker}: {market_data['Close'].tolist()} and suggest an investment strategy."
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text if response else "No insights available."

def fetch_financial_news():
    url = "https://newsapi.org/v2/top-headlines?category=business&apiKey=15f5d8e904543078d3d727b293636fc"
    try:
        response = requests.get(url).json()
        articles = response.get("articles", [])
        return [article["title"] for article in articles[:5]] if articles else ["No news available"]
    except Exception as e:
        return ["Error fetching news: " + str(e)]

def analyze_news_sentiment(news_list):
    sentiments = {'Positive': 0, 'Neutral': 0, 'Negative': 0}
    for news in news_list:
        polarity = TextBlob(news).sentiment.polarity
        if polarity > 0:
            sentiments['Positive'] += 1
        elif polarity == 0:
            sentiments['Neutral'] += 1
        else:
            sentiments['Negative'] += 1
    return sentiments

def ai_stock_screener(investment_type):
    prompt = f"Suggest top 3 stocks for a {investment_type} investment strategy."
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.split("\n") if response else ["No stocks available."]

st.title("AI-Powered Investment Strategies - JPMorgan Chase")
option = st.selectbox("Choose a feature:", ["Stock Trend Analysis", "Portfolio Allocation", "Financial News Sentiment", "Stock Screener"])

if option == "Stock Trend Analysis":
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA, GOOG):")
    if st.button("Get AI Insights") and ticker:
        market_data = fetch_market_data(ticker)
        if isinstance(market_data, str):
            st.write(market_data)
        else:
            st.write("### AI Investment Insights:")
            insights = generate_ai_insights(ticker, market_data)
            st.write(insights)
            
            # Plot stock price trend
            st.write("### Stock Price Trend")
            fig, ax = plt.subplots()
            market_data['Close'].plot(ax=ax, label='Closing Price', marker='o')
            market_data['Close'].rolling(window=3).mean().plot(ax=ax, linestyle='dashed', label='3-day MA')
            market_data['Close'].rolling(window=5).mean().plot(ax=ax, linestyle='dotted', label='5-day MA')
            ax.legend()
            st.pyplot(fig)

elif option == "Portfolio Allocation":
    risk_level = st.selectbox("Select Risk Level:", ["Low", "Medium", "High"])
    amount = st.number_input("Investment Amount ($):", min_value=100)
    if st.button("Get AI Allocation"):
        prompt = f"Suggest an investment allocation for a {risk_level} risk profile with ${amount}."
        model = genai.GenerativeModel("gemini-1.5-flash")
        allocation = model.generate_content(prompt)
        st.write("### AI Portfolio Suggestion:")
        if allocation:
            st.write(allocation.text)
            
            # Mocked allocation breakdown
            allocation_data = {'Stocks': 50, 'Bonds': 30, 'Crypto': 20}
            fig, ax = plt.subplots()
            ax.pie(allocation_data.values(), labels=allocation_data.keys(), autopct='%1.1f%%')
            st.pyplot(fig)

elif option == "Financial News Sentiment":
    if st.button("Fetch Latest News"):
        news = fetch_financial_news()
        st.write("### Top Financial News:")
        for item in news:
            st.write(f"- {item}")
            
        # Sentiment analysis
        sentiment_results = analyze_news_sentiment(news)
        st.write("### News Sentiment Analysis")
        fig, ax = plt.subplots()
        sns.barplot(x=list(sentiment_results.keys()), y=list(sentiment_results.values()), ax=ax)
        ax.set_ylabel("Count")
        st.pyplot(fig)

elif option == "Stock Screener":
    investment_type = st.selectbox("Select Investment Type:", ["Growth", "Dividend", "Tech"])
    if st.button("Get AI-Recommended Stocks"):
        stocks = ai_stock_screener(investment_type)
        st.write("### AI-Recommended Stocks:")
        for stock in stocks:
            st.write(f"- {stock}")
        



#AIzaSyBlTtwu9XObXiWynLSRWlZGVU4jEkhm0H8
#815f5d8e904543078d3d727b293636fc