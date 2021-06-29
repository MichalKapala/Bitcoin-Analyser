from Analysers.stock import Stock
from Analysers.indicators import TechnicalIndicators
from Scraper.scraper import Headers

simple_chart_indicators = ["Moving_average"]


class Analyser:
    updating = False
    def __init__(self, company, ticker):
        self.company = company
        self.ticker = ticker
        self.prices_ = None
        self.indicators_ = []
        self.titles_ = {}
        self.headers = Headers(company)
        self.stock = Stock(ticker)
        self.technicalIndicators = TechnicalIndicators()

    def clear(self):
        self.prices_ = None
        self.indicators_.clear()
        self.titles_.clear()

    def update(self, interval, indicators_list):
        self.updating = True
        self.headers.update_headers()
        self.titles_ = self.headers.get_headers()
        self.stock.update_quotes(interval)
        self.prices_ = self.stock.get_quotes()
        self.technicalIndicators.update_indicators(self.prices_)
        self.indicators_ = self.technicalIndicators.get_indicators(indicators_list)
        self.updating = False

    def get_prices(self):
        return self.prices_

    def get_indicators(self):
        return self.indicators_

    def get_indicator(self, indicator):
        return self.indicators_[indicator]

    def get_titles(self):
        return self.titles_

