import dash_bootstrap_components as dbc
from dash import html

from data import data_2020_power_plants_total, top_emitting_states, total_state_facilities_2020, emissions_change

card1 = dbc.Card(
       [
       html.H4(f"Total U.S. Power Plant Emissions in 2020:",
               className='card1-text'),
       html.H6(f"{data_2020_power_plants_total.iloc[0]['Total Power Plant Emissions']:,} metric tons",
       className='card1-text')
       ]
)

card2 = dbc.Card(
    [
    html.H4(f"A substantial decrease of ",
            className='card4-text'),
    html.H6(f"{emissions_change:,} metric tons",
            className='card4-text'),
    html.H6(f"from year 2011 to 2020",
            className="card4-text")
    ]
)

card3 = dbc.Card(
    [
    html.H4(f"Top Emitting States:",
            className='card2-text'),
    html.H6(f"{top_emitting_states}",
            className='card2-text')
    ]
)

card4 = dbc.Card(
    [
    html.H4(f"Total Power Plant Facilites Across the U.S. in 2020:",
            className='card3-text'),
    html.H6(f"{total_state_facilities_2020}",
            className='card3-text')
    ]
)

def create_cards():
    cards = dbc.Container(
        children=[
            html.Br(),
            dbc.Row([
                dbc.Col(
                dbc.Container(
                    className='parent',
                    children=[
                        dbc.Container(
                            className='card-container card1',
                                children=[card1],
                        ),
                        dbc.Container(
                        className='card-container card2 spacer',
                            children=[card2]
                        ),
                        dbc.Container(
                        className='card-container card3 spacer',
                            children=[card3]
                        ),
                        dbc.Container(
                        className='card-container card4 spacer',
                            children=[card4]
                        )
                    ]
                )
                )
            ])
        ])
    return cards