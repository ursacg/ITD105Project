from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
#import base64
#import io

app = Dash(__name__)
df = pd.read_csv('suicide-rate.csv')
#year_list = df['year'].unique()
country_list = df['country'].unique()

app.layout = html.Div([

    html.Div([
        html.H1("Suicide Rates of Countries by Year",
                style={'textAlign': 'center'})
    ]),

    html.Div([
        dcc.Graph(id='csv-map'),
    ]),

    html.Div([
        html.Label([
                    "Selected Year: ",
                    dcc.Dropdown(id='csv-year',
                    #options=[{'label': y, 'value': y} for y in year_list],
                    options=list(range(1986, 2016)),
                    value=2000,
                    searchable=False,
                    clearable=False,
                    style={'width': '40%'}),
                    ]),
    ]),

    html.Div([
        html.Label([
            "Selected Country: ",
            dcc.Dropdown(
                id='csv-country',
                options=[{'label': c, 'value': c} for c in country_list],
                value='Philippines',
                multi=True,
                clearable=False,
                style={'width': '40%'}),
                ]),
        html.Br(),

        html.Label([
            "Selected Age: ",
            dcc.Dropdown(
                id='csv-age',
                options=[
                    {'label': '5-14 years', 'value': '5-14 years'},
                    {'label': '15-24 years', 'value': '15-24 years'},
                    {'label': '25-34 years', 'value': '25-34 years'},
                    {'label': '35-54 years', 'value': '35-54 years'},
                    {'label': '55-74 years', 'value': '55-74 years'},
                    {'label': '75+ years', 'value': '75+ years'},
                ],
                value='5-14 years',
                searchable=False,
                clearable=False,
                style={'width': '40%'}),
                ]),
        html.Br(),

        html.Label([
            "Selected Sex: ",
            dcc.Dropdown(
                id='csv-sex',
                options=[
                    {'label': 'Male', 'value': 'male'},
                    {'label': 'Female', 'value': 'female'}
                ],
                value='male',
                searchable=False,
                clearable=False,
                style={'width': '40%'}),
                ]),
        html.Br(),

        html.Label([
            "Selected Generation: ",
            dcc.Dropdown(
                id='csv-generation',
                options=[
                    {'label': 'G.I. Generation', 'value': 'G.I. Generation'},
                    {'label': 'Silent Generation', 'value': 'Silent'},
                    {'label': 'Baby Boomers Generation', 'value': 'Boomers'},
                    {'label': 'Generation X', 'value': 'Generation X'},
                    {'label': 'Millenials Generation', 'value': 'Millenials'},
                    {'label': 'Generation Z', 'value': 'Generation Z'},
                ],
                value='Generation Z',
                searchable=False,
                clearable=False,
                style={'width': '40%'}),
                ])
    ])

])

@callback(
    Output('csv-map', 'figure'),
    Input('csv-year', 'value')
)
def update_map(selected_year):
    selected_df = df[df.year == selected_year]

    fig = px.choropleth(selected_df,
                        locationmode='ISO-3',
                        locations='country_iso',
                        color='suicides/100k pop',
                        hover_name='country',
                        hover_data=['country_iso', 'suicides/100k pop'],
                        labels={'country_iso': 'Country Code (ISO-3)', 'suicides/100k pop': 'Suicide Rate (per 100k people)'},
                        color_continuous_scale=px.colors.sequential.Plasma,
                        range_color=(0, 225),
                        width=1500,
                        height=550)
    return fig

if __name__ == '__main__':
    app.run(debug=True)