import yfinance as yf


def get_news(symbol):

    stock = yf.Ticker(symbol)

    try:
        return stock.news
    except:
        return []