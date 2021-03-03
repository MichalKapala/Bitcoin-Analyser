from Analysers.text_anaylser import TextAnalyser
from Analysers.stock import Stock
from Config.analyser_config import AnalyserConfig


class Analyser:
    def __init__(self):
        self.config = AnalyserConfig()
        self.text_analyser = TextAnalyser(self.config.get_cfg("Company"))
        self.stock = Stock(self.config.get_cfg("Ticker"))
        self.prices = None

    def process(self):
        peroid = self.config.get_cfg("Peroid")
        interval = self.config.get_cfg("Interval")
        self.text_analyser.update_titles()
        self.stock.update_quotes(peroid, interval)
