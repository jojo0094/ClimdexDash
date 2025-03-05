from dash import Dash, html, Output, Input, dcc
from ..data.source import DataSource
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from ..data.indices import ClimateIndices
import pandas as pd


def barchart_max_n_day_precipitation_amount(data: pd.DataFrame, n: int, freq: str = "YS") -> go.Figure:
    indices = ClimateIndices(data)
    max_n_day_precipitation = indices.max_n_day_precipitation_amount(n, freq)
    return_fig = go.Figure(go.Bar(x=max_n_day_precipitation.time, y=max_n_day_precipitation))
    #yxis = "total precipitation (mm)"
    return_fig.update_layout(title=f"Maximum {n}-day Precipitation Amount", yaxis_title="Total Precipitation (mm)")
    return return_fig

def barchart_maximum_consecutive_wet_days(data: pd.DataFrame, freq: str = "YS") -> go.Figure:
    indices = ClimateIndices(data)
    max_consecutive_wet_days = indices.maximum_consecutive_wet_days(freq)
    return_fig = go.Figure(go.Bar(x=max_consecutive_wet_days.time, y=max_consecutive_wet_days))
    #yxis = "total precipitation (mm)"
    return_fig.update_layout(title=f"Maximum Consecutive Wet Days", yaxis_title="wet days")
    return return_fig

def barchart_maximum_consecutive_dry_days(data: pd.DataFrame, freq: str = "YS") -> go.Figure:
    indices = ClimateIndices(data)
    max_consecutive_dry_days = indices.maximum_consecutive_dry_days(freq)
    return_fig = go.Figure(go.Bar(x=max_consecutive_dry_days.time, y=max_consecutive_dry_days))
    #yxis = "total precipitation (mm)"
    return_fig.update_layout(title=f"Maximum Consecutive Dry Days", yaxis_title="dry days")
    return return_fig


def render(app: Dash, source: DataSource):

    @app.callback(
        Output("time-series-output", "children"),
        Input("map", "clickData"),
        prevent_initial_call=True  # Prevents running the callback before user clicks
    )
    def click_output(clickData) -> html.Div:
        if not clickData:
            return html.Div("Click on the map to load data and wait for the spinner to disappear.")

        lat, lon = clickData['latlng']['lat'], clickData['latlng']['lng']

        data = source.get_timeseries(lat, lon)

        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(
            go.Scatter(
                x=data.time, 
                y=data['total_precipitation'], 
                mode='lines', 
                name='Precipitation'
            ), 
            row=1, col=1
        )
        #yxis = "total precipitation (mm)"
        fig.update_layout(title=f"Time Series for {lat}, {lon}",
                            yaxis_title="Total Precipitation (mm)")

        bar_fig1 = barchart_max_n_day_precipitation_amount(data, 5)
        bar_fig2 = barchart_maximum_consecutive_wet_days(data)
        # bar_fig3 = barchart_maximum_consecutive_dry_days(data)


        return html.Div([
            dcc.Graph(figure=fig),
            dcc.Graph(figure=bar_fig1),
            dcc.Graph(figure=bar_fig2),
            # dcc.Graph(figure=bar_fig3)
        ])

    return html.Div(
        className="time-series",
        children=[
            html.H2("Time Series (Notes: Indices have not been verified; currently based on xclim python package)"),
            dcc.Loading(
                id="loading-time-series",
                type="circle",
                children=html.Div(
                    id="time-series-output",
                    children=html.Div("Click on the map to load data and wait for the spinner to disappear. Note: Distance buffer logic was not applied yet (points outside NZ bounding box will snap to nearest point; please allow up to 1 min of data loading time due to 2-core VM instance :D.")
                )
            )
        ]
    )

