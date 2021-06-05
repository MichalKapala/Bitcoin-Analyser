from Analysers.stock import Stock
import plotly.graph_objects as go
from Analysers.indicators import TechnicalIndicators
from Scraper.scraper import Headers

simple_chart_indicators = ["Moving_average"]


class Analyser:
    def __init__(self, company, ticker):
        self.company = company
        self.ticker = ticker
        self.prices_ = None
        self.indicators_ = []
        self.titles_ = {}
        self.headers = Headers(company)
        self.stock = Stock(ticker)
        self.technical_indicators = TechnicalIndicators()

    def clear(self):
        self.prices_ = None
        self.indicators_.clear()
        self.titles_.clear()

    def update(self, interval, indicators_list):
        self.headers.update_headers()
        self.titles_ = self.headers.get_headers()
        self.stock.update_quotes(interval)
        self.prices_ = self.stock.get_quotes()
        self.updated_indicators(indicators_list)

    def updated_indicators(self, indicators_list):
        self.technical_indicators.calculate_indicators(self.prices_)
        self.indicators_ = self.technical_indicators.get_indicators(indicators_list)

    def get_prices(self):
        return self.prices_

    def get_indicators(self):
        return self.indicators_

    def get_titles(self):
        return self.titles_

