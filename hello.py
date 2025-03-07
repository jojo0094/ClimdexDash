from dash import Dash

from dash_bootstrap_components.themes import BOOTSTRAP

from src.components.layout import create_layout
from src.data.source import DataSource, PostgresDataSource, CSVFileSource

def main() -> None:

    # load the data and create the data manager
    datasource = PostgresDataSource()
    # datasource = CSVFileSource("data/fake_data.csv")

    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.layout = create_layout(app, datasource)
    app.run(debug=True, host="0.0.0.0", port=8050)
2

if __name__ == "__main__":
    main()
app = Dash()
