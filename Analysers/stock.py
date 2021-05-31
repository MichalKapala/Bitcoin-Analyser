import yfinance as yf

interval_map = {"1d": "1m", "5d": "5m", "1mo": "30m",
                "3mo": "1d", "6mo": "1d", "1y": "5d",
                "5y": "5d", "10y": "1wk", "max": "1mo"}

peroid_map = {None: "1d", "2m": "1d", "5m": "5d", "30m": "1mo", "60m": "2mo",
              "1d": "1y", "5d": "5y",
              "1wk": "10y"}


class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.data_ = None

    def update_quotes(self, interval):
        peroid = peroid_map[interval]
        self.data_ = yf.download(tickers=self.ticker, period=peroid, interval=interval)

    def get_quotes(self):
        return self.data_

