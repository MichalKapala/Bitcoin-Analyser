import yfinance as yf


class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.data_ = None

    def update_quotes(self, peroid, interval):
        self.data_ = yf.download(tickers=self.ticker, period=peroid, interval=interval)

    def get_quotes(self):
        return self.data_

