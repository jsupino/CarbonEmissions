import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
from data import emission_sums_by_state, states, total_emissions_per_year

initial_graph = 'Non-Biogenic CO2 Emissions'
initial_map_year = 2011
initial_graph_year = 2011
initial_state = 'Texas'
initial_results = 'Top States'

initial_choropleth = px.choropleth(emission_sums_by_state,
                            locations='State',
                            locationmode='USA-states',
                            color='CO2 emissions (non-biogenic)',
                            color_continuous_scale='deep',
                            range_color=[emission_sums_by_state['CO2 emissions (non-biogenic)'].min(),
                                         emission_sums_by_state['CO2 emissions (non-biogenic)'].max()],
                            scope='usa')


def create_body():
    body_content = dbc.Container(
        children=[
            html.Br(),
            dbc.Row([
                dbc.Col(
                dbc.Container(
                    className='parent',
                    children=[
                        dbc.Container(className='graph-container graph1',
                                      children=[
                            html.H1(
                            ),
                            dcc.Dropdown(
                                id='graph-type',
                                options=[
                                    {'label': 'Facility Count', 'value': 'Facility Count'},
                                    {'label': 'Non-Biogenic CO2 Emissions', 'value': 'Non-Biogenic CO2 Emissions'}
                                ],
                            style={
                                'width': '80%',
                                'display': 'inline-block',
                                'margin-bottom': '10px',
                                'text-align': 'center',
                            },
                            value=initial_graph
                            ),
                            dcc.Dropdown(
                                id='top-bottom',
                                options=[
                                    {'label': 'Top 25 States', 'value': 'Top States'},
                                    {'label': 'Bottom 25 States', 'value': 'Bottom States'},
                                ],
                            style={
                                'width': '80%',
                                'display': 'inline-block',
                                'margin-bottom': '10px',
                                'text-align': 'center',
                            },
                            value=initial_results
                            ),
                            dcc.Slider(
                                id='year-slider',
                                min=2011,
                                max=2020,
                                step=1,
                                value=initial_graph_year,
                                marks={2011: '2011', 2012: '2012', 2013: '2013', 2014: '2014',
                                       2015: '2015', 2016: '2016', 2017: '2017', 2018: '2018',
                                       2019: '2019', 2020: '2020'},
                            ),
                            dcc.Graph(
                                id = 'data-graph',
                            ),
                            dcc.Store(id='initial-values',
                                    data={'graph_type': initial_graph,
                                        'year': initial_graph_year,
                                        'results': initial_results}
                                    ),
                        ],
                    ),
                    dbc.Container(
                        className='graph-container graph2 spacer',
                            children=[
                            html.H1(
                                    ),
                                dcc.Graph(
                                    id='choropleth-map',
                                    style={
                                        'height': '600px',  
                                        'width': '100%',    
                                        'margin': '0px'
                                    },
                                    config={
                                        'displayModeBar': False,  # Hide the mode bar
                                        'displaylogo': False,     # Hide the plotly logo 
                                        'responsive': True,       # Make the graph responsive
                                        'legend': {'x': 0, 'y': 1, 'traceorder': 'normal', 'orientation': 'h'},
                                    }
                                    ),
                                dcc.Store(
                                    id='initial-choropleth',
                                    data=initial_choropleth
                                    ),
                                html.Button(id='play-button', n_clicks=0, style={'display': 'none'}),
                                ],
                                style={
                                    'width': '100%',
                                    'display': 'inline-block'
                                }
                            ),]
                        )
                    )
                ]),

            html.Br(),

            dbc.Row([   
                dbc.Col(
                    dbc.Container(
                        className='parent',
                        children=[
                            dbc.Container(
                                className="graph-container graph3",
                                children=[
                                    html.H2(children='Thirty Largest Facilities By State',
                                            style={'font-family': 'Garamond', 'font-size': '20px', 'color': 'rgb(3, 44, 97)'}),
                                    dcc.Dropdown(
                                        id='state-selection',
                                        placeholder='Select a State',
                                        style={
                                            'backgroundColor': 'white',
                                            'color': '#1C5699',
                                            'width': '80%',
                                            'height': '40px',
                                            'display': 'inline-block',
                                            'alignItems': 'center',
                                            'text-align': 'center'
                                            },
                                        options= [{'label': state, 'value': state} for state in states],
                                        value=initial_state
                                    ),
                                    dcc.Slider(
                                        id='map-year-slider',
                                        min=2011,
                                        max=2020,
                                        step=1,
                                        value=initial_map_year,
                                        marks={2011: '2011', 2012: '2012', 2013: '2013', 2014: '2014',
                                               2015: '2015', 2016: '2016', 2017: '2017', 2018: '2018',
                                               2019: '2019', 2020: '2020'}
                                    ),
                                    dcc.Graph(
                                        id='map',
                                        style={
                                            'width': '100%',
                                            'display':'inline-block'
                                        }
                                    ),
                                ]
                            ),
                            dbc.Container(
                                className='graph-container graph4',
                                children=[
                                    html.H2(children='Trend of Annual Emissions Across the United States',
                                        style={'font-family': 'Garamond', 'font-size': '20px', 'color': 'rgb(3, 44, 97)'}),
                                    dcc.Graph(
                                        id='line',
                                        style={'width': '100%',
                                               'display': 'flex'},
                                        figure = px.line(total_emissions_per_year,
                                                         x='Year',
                                                         y='CO2 emissions (non-biogenic)'
                                                        ).update_layout(
                                                                        xaxis_title='Year',
                                                                        yaxis_title='Non-Biogenic Emissions (metric tons CO2e)',
                                                                        plot_bgcolor='#EDEEEE',
                                                                        # font=dict(family='Garamond', size=12, color='black')
                                                                        ).update_traces(
                                                                            line_color='#1C5699',
                                                                            # opacity= 0.6,
                                                                            line_width=5
                                                                            )
                                    ),
                                ]
                            )
                        ])
                    )
                ]  
            )
        ])
    return body_content
