import yfinance as yf

def get_stock_data(symbol, period):

    stock = yf.Ticker(symbol)

    history = stock.history(period=period)

    try:
        info = stock.fast_info
    except:
        info = {}

    return info, history