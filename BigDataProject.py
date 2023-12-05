from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

app = Dash(__name__)
df = pd.read_csv('suicide-rate.csv')

app.layout = html.Div([
    html.Div([
        html.H1("Suicide Rates by Year", style={'textAlign': 'center'})
    ]),
    html.Div([
        dcc.Graph(id='csv-graph'),
    ]),
    html.Div([
        dcc.Input(id='csv-year', type='number', inputMode='numeric', value=1999,
                  max=2010, min=1987, step=1, required=True),
        html.Div(id='csv-output-info'),
    ], style={'text-align': 'center'}),
])

@callback(
    Output('csv-graph', 'figure'),
    Input('csv-year', 'value')
)

def update_map(selected_year):
    selected_df = df[df.year == selected_year]

    fig = px.choropleth(selected_df,
                        locations='country',
                        color='suicides/100k pop',
                        hover_name='country')

if __name__ == '__main__':
    app.run(debug=True)