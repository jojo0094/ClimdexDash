import dash_leaflet as dl
from dash import Dash, html, Output, Input


def render(app: Dash ) -> html.Div:

    @app.callback(Output("map", "viewport"), Input("btn", "n_clicks"), prevent_initial_call=True)
    def fly_to_wellington(_):
        return dict(center=[-41.28664, 174.77557],
                    zoom=10, transition="flyTo")

    #use clickData to get the clicked point lat and lon to id="output"
    @app.callback(Output("output", "children"), Input("map", "clickData"))
    def click_output(clickData):
        return f"You clicked on lat: {clickData['latlng']}"

    return html.Div(
        className="map-plan",
        children=[
            dl.Map([
                dl.TileLayer()
            ], center=[-41, 174], zoom=4, style={'height': '50vh'}, id="map"),
            html.Button("Fly to Wellington", id="btn"),
            html.Div(id="output")
        ]
    )
