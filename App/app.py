from Analysers.analyser import Analyser
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objects as go

peroid_options = [
    {"label": "2 minute", "value": "2m"},
    {"label": "5 minutes", "value": "5m"},
    {"label": "30 minutes", "value": "30m"},
    {"label": "1 hour", "value": "60m"},
    {"label": "1 day", "value": "1d"},
    {"label": "5 days", "value": "5d"},
    {"label": "1 week", "value": "1wk"},
]

indicators_options = [
    {"label": "Moving Average", "value": "Moving_average"},
    {"label": "Bollinger_bands", "value": "Bollinger_bands"},
    {"label": "Weighted moving average", "value": "Weighted_MA"},
    {"label": "Exponential moving average", "value": "Exp_MA"},
]

complex_chart_indicators = ["Bollinger_bands"]
constant_indicators = ["RSI"]
simple_chart_indicators = ["Moving_average", "Weighted_MA", "Exp_MA"]
company = "Bitcoin"  # temporary hardcoded value
ticker = "BTC-USD"  # temporary hardcoded value
default_interval = "2m"

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
analyser = Analyser(company, ticker)
analyser.update(default_interval, constant_indicators)


def create_chart(prices: pd.DataFrame, indicators: dict):
    index = prices.index

    # Visualzie prices
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=index,
                open=prices["Open"],
                high=prices["High"],
                low=prices["Low"],
                close=prices["Close"],
            )
        ],
    )

    # Visualize indicators on figure
    for indicator in indicators:
        if indicator in simple_chart_indicators:
            indicator_data = indicators[indicator]
            start = index.shape[0] - indicator_data.shape[0]
            index = index[start:]
            fig.add_trace(go.Scatter(x=index, y=indicator_data, mode="lines"))
        elif indicator in complex_chart_indicators:
            indicator_data_d = indicators[indicator][0]
            indicator_data_h = indicators[indicator][1]
            start = index.shape[0] - indicator_data_h.shape[0]
            index = index[start:]
            fig.add_trace(go.Scatter(x=index, y=indicator_data_d, mode="lines"))
            fig.add_trace(go.Scatter(x=index, y=indicator_data_h, mode="lines"))

    fig.update_layout(height=800, yaxis=dict(fixedrange=False))
    return fig


def create_const_ind_comp(indicators):
    indicators_list = []
    component = lambda ind, value: html.Div(
        children=[html.P(children="{}: {}".format(ind, str(value))), html.Br()]
    )
    for key in indicators:
        indicators_list.append(component(key, analyser.get_indicator(key)))
    return indicators_list


def create_headers():
    return html.Div(
        children=[
            html.Ul(
                children=[
                    html.Li(dcc.Link(title, href=link))
                    for title, link in analyser.get_titles().items()
                ]
            )
        ]
    )


headerDiv = html.Div([html.H1(company, className="h1", id="title")], id="mainHeader")

dropdownDiv = html.Div(
    [
        dcc.Dropdown(
            options=peroid_options,
            value=default_interval,
            className="dropdown",
            id="peroid_drop",
        ),
        dcc.Dropdown(
            options=indicators_options,
            multi=True,
            placeholder="Select indicators",
            className="dropdown",
            id="indicators_drop",
        ),
    ],
    id="graphDrop",
)
fig = create_chart(analyser.get_prices(), analyser.get_indicators())

indicatorsDiv = html.Div(
    create_const_ind_comp(constant_indicators), id="indicatorsDiv"
)

graphDiv = html.Div(
    [dropdownDiv, dcc.Graph(id="main_graph", figure=fig)], id="graphDiv"
)

mainDiv = html.Div([graphDiv])

app.layout = html.Div(
    [
        headerDiv,
        mainDiv,
        html.H2(
            children="Technical analysis",
        ),
        html.Div(id="tech_anal;", children=[]),
        indicatorsDiv,
        html.Br(),
        html.H2(
            children="Headers",
        ),
        create_headers(),
        html.H2(
            children="Recommendation",
        ),
        dcc.Interval(id="interval-component", interval=3 * 1000),
    ],
    id="mainLayout",
)


@app.callback(
    Output(component_id="main_graph", component_property="figure"),
    Output(component_id="indicatorsDiv", component_property="children"),
    Input(component_id="interval-component", component_property="'n_intervals'"),
    Input(component_id="peroid_drop", component_property="value"),
    Input(component_id="indicators_drop", component_property="value"),
)
def update_data(n, peroid, indicators_list):
    if not Analyser.updating:
        update_ind = []
        if type(indicators_list) == list:
            update_ind = indicators_list + constant_indicators
        else:
            update_ind = constant_indicators
        analyser.clear()
        analyser.update(peroid, update_ind)
        fig = create_chart(analyser.get_prices(), analyser.get_indicators())
        indicatorsDiv = html.Div(
            create_const_ind_comp(constant_indicators), id="indicatorsDiv"
        )
    return fig, indicatorsDiv


def process():
    app.run_server(debug=True)


if __name__ == "__main__":
    process()
