from Analysers.text_anaylser import TextAnalyser
from Analysers.stock import Stock


class Analyser:
    def __init__(self, company, ticker):
        self.company = company
        self.ticker = ticker
        self.text_analyser = TextAnalyser(company)
        self.stock = Stock(ticker)

    def process(self):
        pass
