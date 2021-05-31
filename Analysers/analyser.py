from Analysers.stock import Stock
import plotly.graph_objects as go
from Analysers.technical_analyser import TechnicalAnalyser
from Scraper.scraper import Headers

simple_chart_indicators = ["Moving_average"]


class Analyser:
    def __init__(self, company, ticker):
        self.company = company
        self.ticker = ticker
        self.headers = Headers(self.company)
        self.stock = Stock(ticker)
        self.technical_analyser = TechnicalAnalyser()
        self.prices = []
        self.indicators = []
        self.titles = {}

    def clear(self):
        self.prices = []
        self.indicators = []
        self.titles = {}

    def update(self, interval, indicators_list):
        self.headers.update_headers()
        self.titles = self.headers.get_headers()
        self.stock.update_quotes(interval)
        self.prices = self.stock.get_quotes()
        self.updated_indicators(indicators_list)

    def create_chart(self):
        index = self.prices.index
        start = index[0]
        stop = index[-1]
        day_diff = (stop - start).total_seconds() / 86400

        #Visualzie prices
        fig = go.Figure(data=[go.Candlestick(x=index,
                        open=self.prices["Open"],
                        high=self.prices["High"],
                        low=self.prices["Low"],
                        close=self.prices["Close"])],)

        #Visualize indicators on figure
        fig = self.visualize_indicators(fig, index)
        fig.update_layout(height=800, yaxis=dict(fixedrange=False))

        return fig

    def updated_indicators(self, indicators_list):
        self.technical_analyser.calculate_indicators(self.prices)
        self.indicators = self.technical_analyser.get_indicators(indicators_list)

    def visualize_indicators(self, fig, index):
        for indicator in self.indicators:
            if indicator in simple_chart_indicators:
                indicator_data = self.indicators[indicator]
                start = index.shape[0] - indicator_data.shape[0]
                index = index[start:]
                fig.add_trace(go.Scatter(x=index, y=indicator_data, mode='lines'))
            elif indicator == "Bollinger_bands":
                indicator_data_d = self.indicators[indicator][0]
                indicator_data_h = self.indicators[indicator][1]
                start = index.shape[0] - indicator_data_h.shape[0]
                index = index[start:]
                fig.add_trace(go.Scatter(x=index, y=indicator_data_d, mode='lines'))
                fig.add_trace(go.Scatter(x=index, y=indicator_data_h, mode='lines'))
        return fig
