from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
#import base64
#import io

app = Dash(__name__)
df = pd.read_csv('suicide-rate.csv')
year_list = df['year'].unique()

app.layout = html.Div([

    html.Div([
        html.H1("Suicide Rates of Countries by Year",
                style={'textAlign': 'center'})
    ]),

    html.Div([
        dcc.Graph(id='csv-map'),
    ]),

    html.Div([
        html.P("Selected Year: "),
        dcc.Dropdown(id='csv-year',
                     options=[{'label': y, 'value': y} for y in year_list],
                     value=2000,
                     searchable=False,
                     clearable=False,
                     style={'width': '40%'}),
    ]),

])

@callback(
    Output('csv-map', 'figure'),
    Input('csv-year', 'value')
)
def update_map(selected_year):
    selected_df = df[df.year == selected_year]

    fig = px.choropleth(selected_df,
                        locations='country_iso',
                        color='suicides/100k pop',
                        hover_name='country',
                        color_continuous_scale=px.colors.sequential.Plasma)
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)