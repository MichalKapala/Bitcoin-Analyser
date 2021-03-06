from Analysers.text_anaylser import TextAnalyser
from Analysers.stock import Stock
from Config.analyser_config import AnalyserConfig
import plotly.graph_objects as go
from Analysers.technical_analyser import TechnicalAnalyser


class Analyser:
    def __init__(self):
        self.config = AnalyserConfig()
        self.company = self.config.get_cfg("Company")
        self.text_analyser = TextAnalyser(self.company)
        self.stock = Stock(self.config.get_cfg("Ticker"))
        self.technical_analyser = TechnicalAnalyser(self.config)
        self.prices = None
        self.indicators = None
        self.titles = []
        self.company = self.config.get_cfg("Company")

    def process(self):
        peroid = self.config.get_cfg("Peroid")
        interval = self.config.get_cfg("Interval")
        self.text_analyser.update_titles()
        self.titles = self.text_analyser.get_titles()
        self.stock.update_quotes(peroid, interval)
        self.prices = self.stock.get_quotes()
        self.updated_indicators()
        self.create_chart()

    def create_chart(self):
        data = self.stock.get_quotes()
        ticker = self.config.get_cfg("Ticker")
        index = data.index
        fig = go.Figure(data=[go.Candlestick(x=index,
                        open=data["Open"],
                        high=data["High"],
                        low=data["Low"],
                        close=data["Close"])])
        fig.layout = dict(title=ticker, height=600)

        return fig

    def update_titles(self):
        self.titles = self.text_analyser.get_titles()

    def updated_indicators(self):
        self.technical_analyser.calculate_indicators(self.prices)
        self.indicators = self.technical_analyser.get_indicators()

