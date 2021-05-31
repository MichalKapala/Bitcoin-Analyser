from Analysers.analyser import Analyser
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import numpy as np

peroid_options = [{'label': "2 minute", 'value': "2m"},
                 {'label': "5 minutes", 'value': "5m"},
                 {'label': "30 minutes", 'value': "30m"},
                 {'label': "1 hour", 'value': "60m"},
                  {'label': "1 day", 'value': "1d"},
                 {'label': "5 days", 'value': "5d"},
                 {'label': "1 week", 'value': "1wk"}]

indicators_options = [{'label': "RSI", 'value': "RSI"},
                      {'label': "Moving Average", 'value': "Moving_average"},
                      {'label': "Bollinger_bands", 'value': "Bollinger_bands"}
                      ]

indicators_to_write = ["RSI"]

company = "Bitcoin" # temporary hardcoded value
ticker = "BTC-USD"   # temporary hardcoded value
default_interval = "2m"
app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
analyser = Analyser(company, ticker)
analyser.update(default_interval, [])
fig = analyser.create_chart()

def create_indicators_component(indicators):
    indicators_list = []
    component = lambda ind, value: html.Div(children=[html.P(children="{}: {}".format(ind, str(value))), html.Br()])
    for indicator in indicators:
        if indicator in indicators_to_write:
            indicator_val = indicators[indicator]
            if type(indicator_val) == np.ndarray:
                indicator_val = indicator_val[-1]
                indicators_list.append(component(indicator, indicator_val))
            else:
                indicators_list.append(component(indicator, indicator_val))
    return indicators_list


def create_headers():
    return html.Div(
            children=[html.Ul(
                children=[html.Li(dcc.Link(title, href=link)) for title, link in analyser.titles.items()])])


headerDiv = html.Div([html.H1(company, className="h1", id="title")],id="mainHeader")

dropdownDiv = html.Div([dcc.Dropdown(options=peroid_options,
                            value=default_interval, className="dropdown", id="peroid_drop"),
                        dcc.Dropdown(options=indicators_options,
                            multi=True,
                            placeholder="Select indicators", className="dropdown", id="indicators_drop")],
                        id="graphDrop")

graphDiv = html.Div([dropdownDiv, dcc.Graph(id="main_graph", figure=fig)])

mainDiv = html.Div([graphDiv])


app.layout = html.Div([
            headerDiv,
            mainDiv,
            html.H2(children='Indicators', ),
            html.Div(id='indicators', children=[]),
            html.Br(),
            html.H2(children='Headers', ),
            create_headers(),
            html.H2(children='Recommendation', )
        ], id="mainLayout")


@app.callback(
    Output(component_id='main_graph', component_property='figure'),
    Output(component_id='indicators', component_property='children'),
    Input(component_id='peroid_drop', component_property='value'),
    Input(component_id='indicators_drop', component_property='value'))
def update_data(peroid, indicators_list):
    analyser.clear()
    analyser.update(peroid, indicators_list)
    fig = analyser.create_chart()
    indicators = analyser.indicators
    indicators_components = create_indicators_component(indicators)
    return fig, indicators_components


def process():
    app.run_server(debug=True)


if __name__ == "__main__":
    process()