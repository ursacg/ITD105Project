# Import packages for app
from dash import Dash, dcc, html, Input, Output, callback
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
#from simpledbf import Dbf5

# Initialize Dash app
app = Dash(__name__)

# Load initial data
df = pd.read_csv('suicide-rate.csv')

# Create country list for dropdown
country_list = [{'label': c, 'value': c} for c in df['country'].unique()]

# App layout
app.layout = html.Div([

    # Page title
    html.Div([
        html.H1("Suicide Rate of Countries Based on Age and Sex (1986-2015)",
                style={'textAlign': 'center'})
    ]),

    # File upload
    html.Div([
        html.Hr(),
        html.H3("Upload CSV or DBF file"),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select File')
            ]),
            multiple=False,
            style={
                'width': '50%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'solid',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
        ),
        html.Div(id='output-upload-data'),
    ]),

    # Data selection
    html.Div([

        # Year selection
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

        # Age selection
        html.Label([
                    "Selected Age: ",
                    dcc.Dropdown(id='csv-age',
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

        # Sex selection
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

            ]),

    # Choropleth map output
    html.Div([
        dcc.Graph(id='csv-map'),
    ]),

    html.Div([
        html.Hr(),
        html.H2("No. of Suicides, Population, Yearly GDP, and Yearly GDP per Capita of a Country",
                style={'textAlign': 'center'})
    ]),

    # Country selection
    html.Div([
        html.Label([
            "Selected Country: ",
            dcc.Dropdown(
                id='csv-country',
                options=country_list,
                value=['Philippines',
                       'South Africa',
                       'Brazil',
                       'United States',
                       'France',
                       'Australia'],
                multi=True,
                clearable=False,
                style={'width': '50%'}
                ),
                ]),

    ]),

    # No. of suicides line graph output
    html.Div([
        dcc.Graph(id='csv-graph-suicides')
    ]),

    # Population line graph output
    html.Div([
        dcc.Graph(id='csv-graph-population')
    ]),

    # GDP per year line graph output
    html.Div([
        dcc.Graph(id='csv-graph-gdp-year')
    ]),

    # GDP per capita line graph output
    html.Div([
        dcc.Graph(id='csv-graph-gdp-capita')
    ]),

    html.Div([
        html.Hr()
    ]),

    html.Div([
        html.H2("Predicted Rates ",
                style={'textAlign': 'center'})
    ]),

    html.Div([
        dcc.Graph(id='csv-graph-predict-suicide-rate')
    ]),

])

@callback(
    Output('csv-map', 'figure'),
    Input('csv-year', 'value'),
    Input('csv-age', 'value'),
    Input('csv-sex', 'value')
)
def update_map(selected_year, selected_age, selected_sex):
    selected_df = df[(df.year == selected_year) &
                     (df.age == selected_age) &
                     (df.sex == selected_sex)]

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
    [Input('csv-country', 'value')],
    Input('csv-age', 'value'),
    Input('csv-sex', 'value')
)
def update_graph_suicide(selected_country, selected_age, selected_sex):
    selected_df = df[(df['country'].isin(selected_country)) &
                     (df.age == selected_age) &
                     (df.sex == selected_sex)]

    fig = px.line(selected_df,
                  x='year',
                  y='suicides_no',
                  color='country',
                  labels={
                      'year': 'Year',
                      'suicides_no': 'No. of Suicides',
                      'country': 'Selected Country'
                  },
                  title='No. of Suicides Based on Age and Sex',
                  markers=True)
    return fig

@callback(
    Output('csv-graph-population', 'figure'),
    [Input('csv-country', 'value')],
    Input('csv-age', 'value'),
    Input('csv-sex', 'value')
)
def update_graph_population(selected_country, selected_age, selected_sex):
    selected_df = df[(df['country'].isin(selected_country)) &
                     (df.age == selected_age) &
                     (df.sex == selected_sex)]

    fig = px.line(selected_df,
                  x='year',
                  y='population',
                  color='country',
                  labels={
                      'year': 'Year',
                      'population': 'Population',
                      'country': 'Selected Country'
                  },
                  title='Population Based on Age and Sex',
                  markers=True)
    return fig

@callback(
    Output('csv-graph-gdp-year', 'figure'),
    [Input('csv-country', 'value')],
    Input('csv-age', 'value'),
    Input('csv-sex', 'value')
)
def update_graph_gdp_year(selected_country, selected_age, selected_sex):
    selected_df = df.loc[(df['country'].isin(selected_country)) &
                         (df.age == selected_age) &
                         (df.sex == selected_sex)]

    fig = px.line(selected_df,
                  x='year',
                  y='gdp_for_year($)',
                  color='country',
                  labels={
                      'year': 'Year',
                      'gdp_for_year($)': 'GDP per Year ($)',
                      'country': 'Selected Country'
                  },
                  title='Yearly Gross Domestic Product (GDP) Based on Age and Sex',
                  markers=True)
    return fig

@callback(
    Output('csv-graph-gdp-capita', 'figure'),
    [Input('csv-country', 'value')],
    Input('csv-age', 'value'),
    Input('csv-sex', 'value')
)
def update_graph_gdp_capita(selected_country, selected_age, selected_sex):
    selected_df = df.loc[(df['country'].isin(selected_country)) &
                         (df.age == selected_age) &
                         (df.sex == selected_sex)]

    fig = px.line(selected_df,
                  x='year',
                  y='gdp_per_capita($)',
                  color='country',
                  labels={
                      'year': 'Year',
                      'gdp_per_capita($)': 'GDP per Capita ($)',
                      'country': 'Selected Country'
                  },
                  title='Yearly Gross Domestic Product (GDP) per Capita Based on Age and Sex',
                  markers=True)
    return fig

@callback(
    Output('csv-graph-predict-suicide-rate', 'figure'),
    [Input('csv-country', 'value')],
    Input('csv-age', 'value'),
    Input('csv-sex', 'value')
)
def predict_graph_suicide_rate(selected_country, selected_age, selected_sex):
    selected_df = df.loc[(df['country'].isin(selected_country)) &
                         (df.age == selected_age) &
                         (df.sex == selected_sex)]
    
    fig = px.scatter(selected_df,
                     x='year',
                     y='suicides_no',
                     color='country',
                     labels={
                         'year': 'Year',
                         'suicides_no': 'No. of Suicides',
                         'country': 'Selected Country'
                     },
                     title='Predicted Projection oF Suicides Based on Age and Sex',
                     trendline='ols',)
    return fig

if __name__ == '__main__':
    app.run(debug=True)