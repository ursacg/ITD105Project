from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
#import base64
#import io

app = Dash(__name__)
df = pd.read_csv('suicide-rate.csv')
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
                    options=list(range(1986, 2016)),
                    value=2000,
                    searchable=False,
                    clearable=False,
                    style={'width': '50%'}
                    ),
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
                style={'width': '50%'}
                ),
                ]),

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
                style={'width': '50%'}
                ),
                ]),

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
                style={'width': '50%'}
                ),
                ]),

        # html.Label([
        #     "Selected Generation: ",
        #     dcc.Dropdown(
        #         id='csv-generation',
        #         options=[
        #             {'label': 'G.I. Generation', 'value': 'G.I. Generation'},
        #             {'label': 'Silent Generation', 'value': 'Silent'},
        #             {'label': 'Baby Boomers Generation', 'value': 'Boomers'},
        #             {'label': 'Generation X', 'value': 'Generation X'},
        #             {'label': 'Millenials Generation', 'value': 'Millenials'},
        #             {'label': 'Generation Z', 'value': 'Generation Z'},
        #         ],
        #         value='Generation Z',
        #         searchable=False,
        #         clearable=False,
        #         style={'width': '50%'}
        #         ),
        #         ])
    ]),

    html.Div([
        dcc.Graph(id='csv-graph-suicides')
    ]),

    html.Div([
        dcc.Graph(id='csv-graph-population')
    ]),

    html.Div([
        dcc.Graph(id='csv-graph-gdp-year')
    ]),

    html.Div([
        dcc.Graph(id='csv-graph-gdp-capita')
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

@callback(
    Output('csv-graph-suicides', 'figure'),
    Input('csv-country', 'value'),
    Input('csv-age', 'value'),
    Input('csv-sex', 'value')
)
def update_graph_suicide(selected_country, selected_age, selected_sex):
    selected_df = df[df.country == selected_country][df.age == selected_age][df.sex == selected_sex]

    fig = px.line(selected_df,
                  x='year',
                  y='suicides_no',
                  color='country',
                  labels={
                      'year': 'Year',
                      'suicides_no': 'No. of Suicides',
                      'country': 'Selected Country'
                  },
                  title='No. of Suicides in a Country Based on Age and Sex',
                  markers=True)
    return fig

@callback(
    Output('csv-graph-population', 'figure'),
    Input('csv-country', 'value'),
    Input('csv-age', 'value'),
    Input('csv-sex', 'value')
)
def update_graph_population(selected_country, selected_age, selected_sex):
    selected_df = df[df.country == selected_country][df.age == selected_age][df.sex == selected_sex]

    fig = px.line(selected_df,
                  x='year',
                  y='population',
                  color='country',
                  labels={
                      'year': 'Year',
                      'population': 'Population',
                      'country': 'Selected Country'
                  },
                  title='Population of a Country Based on Age and Sex',
                  markers=True)
    return fig

@callback(
    Output('csv-graph-gdp-year', 'figure'),
    Input('csv-country', 'value'),
    Input('csv-age', 'value'),
    Input('csv-sex', 'value')
)
def update_graph_gdp_year(selected_country, selected_age, selected_sex):
    selected_df = df[df.country == selected_country][df.age == selected_age][df.sex == selected_sex]

    fig = px.line(selected_df,
                  x='year',
                  y='gdp_for_year($)',
                  color='country',
                  labels={
                      'year': 'Year',
                      'gdp_for_year($)': 'GDP per Year ($)',
                      'country': 'Selected Country'
                  },
                  title='Yearly Gross Domestic Product (GDP) of a Country Based on Age and Sex',
                  markers=True)
    return fig

@callback(
    Output('csv-graph-gdp-capita', 'figure'),
    Input('csv-country', 'value'),
    Input('csv-age', 'value'),
    Input('csv-sex', 'value')
)
def update_graph_gdp_capita(selected_country, selected_age, selected_sex):
    selected_df = df[df.country == selected_country][df.age == selected_age][df.sex == selected_sex]

    fig = px.line(selected_df,
                  x='year',
                  y='gdp_per_capita($)',
                  color='country',
                  labels={
                      'year': 'Year',
                      'gdp_per_capita($)': 'GDP per Capita ($)',
                      'country': 'Selected Country'
                  },
                  title='Yearly Gross Domestic Product (GDP) per Capita of a Country Based on Age and Sex',
                  markers=True)
    return fig

if __name__ == '__main__':
    app.run(debug=True)