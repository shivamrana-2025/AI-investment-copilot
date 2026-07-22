import yfinance as yf

def compare_stocks(stock1, stock2, period):

    print(stock1)
    print(stock2)

    ticker1 = yf.Ticker(stock1)
    ticker2 = yf.Ticker(stock2)

    history1 = ticker1.history(period=period)
    history2 = ticker2.history(period=period)

    print(history1.head())
    print(history2.head())

    info1 = ticker1.info
    info2 = ticker2.info

    return history1, history2, info1, info2