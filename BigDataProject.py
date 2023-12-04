from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Suicide Rates of Countries from 1987 to 2014", style={'textAlign': 'center'}),
    html.Div(children=[
        html.Label("Insert CSV file URL here: "),
        dcc.Input(id='file-input', value='csv url file', type='url', style={'margin-left': '5px'})
        ], style={'justifyContent': 'center', 'display': 'flex'}
    ),
    html.P("choropleth map here", style={'textAlign': 'center'})
])

if __name__ == '__main__':
    app.run(debug=True)