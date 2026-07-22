import pandas as pd

stocks = pd.read_csv("stocks.csv")

def search_stocks(search_term: str):
    if not search_term:
        return []

    search_term = search_term.lower()

    matches = stocks[
        stocks["Company"].str.lower().str.contains(search_term) |
        stocks["Symbol"].str.lower().str.contains(search_term)
    ]

    return (
        matches["Company"] + " (" + matches["Symbol"] + ")"
    ).head(6).tolist()