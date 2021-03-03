import yfinance as yf
import pandas as pd
import os

class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.data = None

    def get_quotes(self, peroid, interval):
        self.data = yf.download(tickers=self.ticker, period=peroid, interval=interval)

