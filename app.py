import altair as alt
from dash import Dash, html, dcc, Input, Output
import pandas as pd


df = pd.read_csv("fifa-21.csv")
num_cols = ["Age", "Potential", "Value", "Wage"]


def plot_altair(value):
    chart1 = (
        alt.Chart(
            df,
            title="Visualizing player stats in Premier League",
        )
        .mark_circle(size=20)
        .encode(
            x=alt.X(value, scale=alt.Scale(zero=False)),
            y=alt.Y("Overall", scale=alt.Scale(zero=False)),
            tooltip="Name",
        )
        .properties(height=300)
    )

    chart2 = (
        alt.Chart(df, title=f"Mean {value} rating in premier league teams")
        .mark_bar()
        .encode(x=f"mean({value})", y="Club")
        .properties(height=300)
    )
    return (chart1 | chart2).to_html()


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div(
    [
        dcc.Dropdown(
            id="xcol", value="Age", options=[{"label": i, "value": i} for i in num_cols]
        ),
        html.Iframe(
            id="scatter",
            srcDoc=plot_altair("Age"),
            style={"border-width": "0", "width": "100%", "height": "400px"},
        ),
    ]
)


@app.callback(
    Output("scatter", "srcDoc"),
    Input("xcol", "value"),
)
def update_output(value):
    return plot_altair(value)


if __name__ == "__main__":
    app.run_server(debug=True)
