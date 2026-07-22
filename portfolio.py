import yfinance as yf

def portfolio(stock, qty, buy_price):

    ticker = yf.Ticker(stock)

    current_price = ticker.info.get("currentPrice", 0)

    investment = qty * buy_price

    current_value = qty * current_price

    profit = current_value - investment

    percent = (profit / investment) * 100

    return {
        "current_price": current_price,
        "investment": investment,
        "current_value": current_value,
        "profit": profit,
        "percent": percent
    }