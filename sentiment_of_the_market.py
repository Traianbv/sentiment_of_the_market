import requests
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Download VADER lexicon
nltk.download('vader_lexicon')


def get_yahoo_finance_headlines():
    url = 'https://finance.yahoo.com'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = [item.get_text() for item in soup.find_all('h3')]
    return headlines


def get_reuters_headlines():
    url = 'https://www.reuters.com/finance'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = [item.get_text() for item in soup.find_all('h3', class_='story-title')]
    return headlines


def get_bloomberg_headlines():
    url = 'https://www.bloomberg.com/markets'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = [item.get_text() for item in soup.find_all('h3')]
    return headlines


def get_dailyfx_headlines():
    url = 'https://www.dailyfx.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = [item.get_text() for item in soup.find_all('h3')]
    return headlines


def get_coindesk_headlines():
    url = 'https://www.coindesk.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = [item.get_text() for item in soup.find_all('h3')]
    return headlines


def get_wsj_headlines():
    url = 'https://www.wsj.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = [item.get_text() for item in soup.find_all('h3')]
    return headlines


def get_combined_headlines():
    headlines = []
    try:
        headlines.extend(get_yahoo_finance_headlines())
    except Exception as e:
        print(f"Error fetching Yahoo Finance headlines: {e}")

    try:
        headlines.extend(get_reuters_headlines())
    except Exception as e:
        print(f"Error fetching Reuters headlines: {e}")

    try:
        headlines.extend(get_bloomberg_headlines())
    except Exception as e:
        print(f"Error fetching Bloomberg headlines: {e}")

    try:
        headlines.extend(get_dailyfx_headlines())
    except Exception as e:
        print(f"Error fetching DailyFX headlines: {e}")

    try:
        headlines.extend(get_coindesk_headlines())
    except Exception as e:
        print(f"Error fetching CoinDesk headlines: {e}")

    try:
        headlines.extend(get_wsj_headlines())
    except Exception as e:
        print(f"Error fetching WSJ headlines: {e}")

    return headlines


def categorize_headlines(headlines):
    stock_keywords = ['stock', 'shares', 'market', 'equity']
    crypto_keywords = ['crypto', 'bitcoin', 'ethereum', 'blockchain', 'coin']

    stock_headlines = [headline for headline in headlines if
                       any(keyword in headline.lower() for keyword in stock_keywords)]
    crypto_headlines = [headline for headline in headlines if
                        any(keyword in headline.lower() for keyword in crypto_keywords)]

    return stock_headlines, crypto_headlines


def analyze_sentiment(headlines):
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = [sia.polarity_scores(headline) for headline in headlines]
    return sentiment_scores


def aggregate_sentiment(sentiment_scores):
    positive = sum(1 for score in sentiment_scores if score['compound'] > 0.05)
    neutral = sum(1 for score in sentiment_scores if -0.05 <= score['compound'] <= 0.05)
    negative = sum(1 for score in sentiment_scores if score['compound'] < -0.05)

    total = len(sentiment_scores)
    if total == 0:
        return 0, 0, 0  # Return neutral if no sentiment scores are available

    return (positive / total) * 100, (neutral / total) * 100, (negative / total) * 100


def classify_market(positive_pct, neutral_pct, negative_pct):
    if positive_pct > max(neutral_pct, negative_pct):
        return 'Bullish', positive_pct
    elif negative_pct > max(positive_pct, neutral_pct):
        return 'Bearish', negative_pct
    else:
        return 'Neutral', neutral_pct


def main():
    headlines = get_combined_headlines()
    stock_headlines, crypto_headlines = categorize_headlines(headlines)

    stock_sentiment_scores = analyze_sentiment(stock_headlines)
    crypto_sentiment_scores = analyze_sentiment(crypto_headlines)

    stock_positive_pct, stock_neutral_pct, stock_negative_pct = aggregate_sentiment(stock_sentiment_scores)
    crypto_positive_pct, crypto_neutral_pct, crypto_negative_pct = aggregate_sentiment(crypto_sentiment_scores)

    stock_market_sentiment, stock_market_pct = classify_market(stock_positive_pct, stock_neutral_pct,
                                                               stock_negative_pct)
    crypto_market_sentiment, crypto_market_pct = classify_market(crypto_positive_pct, crypto_neutral_pct,
                                                                 crypto_negative_pct)

    print(f"The market sentiment for stocks is: {stock_market_sentiment} ({stock_market_pct:.2f}%)")
    print(f"The market sentiment for crypto is: {crypto_market_sentiment} ({crypto_market_pct:.2f}%)")
    input('Type any key to exit !')


if __name__ == "__main__":
    main()
