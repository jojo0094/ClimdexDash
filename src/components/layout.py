from dash import Dash, html
from src.components import (
    tp_timeseries,
    indices_card,
    mapPlan,
)

from ..data.source import DataSource


def create_layout(app: Dash, source: DataSource) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className="data-container",
                children=[
                    tp_timeseries.render(app, source),
                    # indices_card.render(app, source),
                ],
            ),
            html.Div(
                className="map-container",
                children=[
                    mapPlan.render(app),
                ],
            ),
        ],
    )
