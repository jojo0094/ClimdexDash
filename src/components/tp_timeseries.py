from dash import Dash, html, Output, Input, dcc

from ..data.source import DataSource
from typing import Tuple
from plotly.subplots import make_subplots
import plotly.graph_objects as go


#render plotly timeseries plot

def render(app: Dash, source: DataSource):

    @app.callback(Output("time-series-output", "children"), Input("map", "clickData"))
    def click_output(clickData) -> html.Div:
        lat, lon = clickData['latlng']['lat'], clickData['latlng']['lng']
        data = source.get_timeseries(lat, lon)
        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(go.Scatter(x=data.time, y=data['total_precipitation'], mode='lines', name='Precipitation'), row=1, col=1)
        fig.update_layout(title=f"Time Series for {lat}, {lon}")
        graph = dcc.Graph(figure=fig)
        return html.Div(graph)

    return html.Div(
        className="time-series",
        children=[
            html.H2("Time Series"),
            html.Div(id="time-series-output")
        ]
    )
