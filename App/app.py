from Analysers.analyser import Analyser
import dash
import dash_html_components as html
import dash_core_components as dcc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


class App:
    def __init__(self):
        self.app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
        self.analyser = Analyser()

    def set_main_layout(self):
        fig = self.analyser.create_chart()
        RSI = self.analyser.indicators["RSI"]
        self.app.layout = html.Div(children=[
            html.H1(children='Stock Analyser',
                    style={
                        'textAlign': 'center',
                    }
                    ),
            html.H2(children='Chart', ),

            dcc.Graph(
                id='example-graph',
                figure=fig
            ),
            html.H2(children='Indicators', ),
            html.P(children="RSI: " + str(RSI)),
            html.Br(),
            html.H2(children='Headers', ),
            self.get_headers(),
            html.H2(children='Recommendation', )
        ])

    def process(self):
        self.analyser.process()
        self.set_main_layout()
        self.app.run_server()

    def get_headers(self):
        return html.Div(
                children=[html.Ul(
                    children=[html.Li(title) for title in self.analyser.titles[:-10]])])
