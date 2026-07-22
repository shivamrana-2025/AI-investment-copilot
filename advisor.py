def investment_advice(history):

    latest = history.iloc[-1]

    ma20 = latest["MA20"]
    ma50 = latest["MA50"]
    close = latest["Close"]

    # Trend
    if ma20 > ma50:
        trend = "Bullish 📈"
    else:
        trend = "Bearish 📉"

    # Recommendation
    if close > ma20 and ma20 > ma50:
        advice = "BUY 🟢"
    elif close < ma20 and ma20 < ma50:
        advice = "SELL 🔴"
    else:
        advice = "HOLD 🟡"

    return trend, advice