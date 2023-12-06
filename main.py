import plotly.express as px
import dash
from dash import html
from dash.dependencies import Input, Output, State
from data import emission_sums_by_state, top_state_facilities_per_year, power_plant_state_year
from header import create_header
from cards import create_cards
from body import create_body

external_stylesheets = ['/assets/styles.css']
app = dash.Dash(__name__, external_stylesheets=['/assets/style.css', 'LUX'])

app.layout = html.Div(id='main', children=[create_header(), create_cards(),
                                           create_body()])

@app.callback(
    Output('map', 'figure'),
    [Input('state-selection', 'value'),
    Input('map-year-slider', 'value')],
    [State('state-selection', 'value'),
    State('year-slider', 'value')]
)
def update_state_map(selected_dropdown_state, selected_slider_year, current_state, current_year):
    """
    Plots the scatter plot of top 30 facilities per state

    Dropdown filters by State Name
    Hover data includes Facility Name, County, Address, City, State, Zip Code, CO2 emissions, Latitude and Longitude

    Returns the State and the top 40 facilites
    """
    selected_state = current_state if selected_dropdown_state is None else selected_dropdown_state
    selected_year = current_year if selected_slider_year is None else selected_slider_year
    filtered_df = top_state_facilities_per_year[
        (top_state_facilities_per_year['State Name'] == selected_state)
        & (top_state_facilities_per_year['Year'] == selected_year)]
    top_facilities_map = px.scatter_geo(filtered_df,
                                        lat='Latitude',
                                        lon='Longitude',
                                        hover_name='Facility Name',
                                        hover_data=['Address', 'City', 'State', 'Zip Code', 'CO2 emissions (non-biogenic)'],
                                        projection='albers usa',
                                        size='CO2 emissions (non-biogenic)',
                                        color='County')
    top_facilities_map.update_geos(center={'lat': filtered_df['Latitude'].mean(),
                                   'lon': filtered_df['Longitude'].mean()},
                                    projection_scale=2.5,
                                    showcoastlines=True,
                                    coastlinecolor='black',
                                    showland=True,
                                    landcolor='#F8EEDA',
                                    showrivers=True,
                                    rivercolor='#AFD1F4',
                                    bgcolor='#AFD1F4')
    return top_facilities_map


@app.callback(
    Output('data-graph', 'figure'),
    [Input('graph-type', 'value'),
     Input('year-slider', 'value'),
    Input('top-bottom', 'value')],
     [State('initial-values', 'data')]
)
def update_graph(selected_graph, selected_year, selected_results, initial_values):
    """
    Plots the bar chart of facility counts and non-biogenic co2 emissions

    Contains two dropdowns:
        Top dropdown filters by facility counts or co2 emissions
        Bottom dropdown filters by top 25 and bottom 25 states

    Returns the corresponding bar chart representing either the top 25 or bottom 25 states based on facility count or co2 emissions
    """
    selected_graph = selected_graph or initial_values['graph_type']
    selected_year = selected_year or initial_values['year']
    selected_results = selected_results or initial_values['results']
    filtered_df = power_plant_state_year[power_plant_state_year['Year'] == int(selected_year)]
    if selected_graph == 'Facility Count' and selected_results == 'Top States':
        sorted_facility_counts = filtered_df.nlargest(25, 'Facility Count').sort_values(by='Facility Count', ascending=False)
        fig = {
            'data': [{'x': sorted_facility_counts['State'], 'y': sorted_facility_counts['Facility Count'],
                     'type': 'bar', 'name': 'Facility Count',
                      'marker': {'color': '#abaff8', 'line': {'color': '#340447', 'width': 1.5, 'opacity': 0.8}}}],
            'layout': {'title': f"Total Facilities Per State in {selected_year}",
                      'xaxis': {'title': ''},
                       'yaxis': {'title': 'Total Facilities'},
                      'plot_bgcolor': '#EDEEEE'}
        }
    elif selected_graph == 'Facility Count' and selected_results == 'Bottom States':
        sorted_facility_counts = filtered_df.nsmallest(25, 'Facility Count').sort_values(by='Facility Count', ascending=False)
        fig = {
            'data': [{'x': sorted_facility_counts['State'], 'y': sorted_facility_counts['Facility Count'],
                     'type': 'bar', 'name': 'Facility Count',
                      'marker': {'color': '#abaff8', 'line': {'color': '#340447', 'width': 1.5, 'opacity': 0.8}}}],
            'layout': {'title': f"Total Facilities Per State in {selected_year}",
                      'xaxis': {'title': ''},
                       'yaxis': {'title': 'Total Facilities'},
                      'plot_bgcolor': '#EDEEEE'}
        }
    elif selected_graph == 'Non-Biogenic CO2 Emissions' and selected_results == 'Top States':
        sorted_co2_emissions = filtered_df.nlargest(25, 'CO2 emissions (non-biogenic)').sort_values(by='CO2 emissions (non-biogenic)', ascending=False)
        fig = {
            'data': [{'x': sorted_co2_emissions['State'], 'y': sorted_co2_emissions['CO2 emissions (non-biogenic)'],
                     'type': 'bar', 'name': 'Non-Biogenic CO2 Emissions',
                      'marker': {'color': '#98D0EB', 'line': {'color': '#1C5699', 'width': 1.5, 'opacity': 0.8}}}],
            'layout': {'title': f"Total Non-Biogenic CO2 Emissions Per State in {selected_year}",
                      'xaxis': {'title': ''},
                       'yaxis': {'title': 'Non-Biogenic CO2 Emissions (MMmt)'},
                        'plot_bgcolor': '#EDEEEE'}
        }
    elif selected_graph == 'Non-Biogenic CO2 Emissions' and selected_results == 'Bottom States':
        sorted_co2_emissions = filtered_df.nsmallest(25, 'CO2 emissions (non-biogenic)').sort_values(by='CO2 emissions (non-biogenic)', ascending=False)
        fig = {
            'data': [{'x': sorted_co2_emissions['State'], 'y': sorted_co2_emissions['CO2 emissions (non-biogenic)'],
                     'type': 'bar', 'name': 'Non-Biogenic CO2 Emissions',
                      'marker': {'color': '#98D0EB', 'line': {'color': '#1C5699', 'width': 1.5, 'opacity': 0.8}}}],
            'layout': {'title': f"Total Non-Biogenic CO2 Emissions Per State in {selected_year}",
                      'xaxis': {'title': ''},
                       'yaxis': {'title': 'Non-Biogenic CO2 Emissions (MMmt)'},
                        'plot_bgcolor': '#EDEEEE'}
        }
    else:
        fig = {}
    return fig

@app.callback(
    Output('choropleth-map', 'figure'),
    Input('play-button', 'play_button')
)
def update_choropleth_map(play_button):
    """
    Plots the interactive choropleth map on the dashboard

    Represents the total emissions for each state by year

    Consists of a play and stop button
    """
    choropleth_map = px.choropleth(emission_sums_by_state,
                        locations='State',
                        locationmode='USA-states',
                        color='CO2 emissions (non-biogenic)',
                        color_continuous_scale='dense',
                        animation_frame='Year',
                        range_color=[emission_sums_by_state['CO2 emissions (non-biogenic)'].min(),
                                        emission_sums_by_state['CO2 emissions (non-biogenic)'].max()],
                        scope='usa')
    choropleth_map.update_layout(
        coloraxis_colorbar=dict(
            title= 'CO2 emissions (MMmt)',
            title_font=dict(size=10),
            len=1,
            thickness=10
            )
        )
    return choropleth_map

if __name__ == '__main__':
    app.run_server(port=1599)

