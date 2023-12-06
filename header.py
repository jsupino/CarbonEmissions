import dash_bootstrap_components as dbc

def create_header():
    header = dbc.Navbar(id = 'navbar', className='navbar', children = [
        dbc.Row([
            dbc.Col(
                dbc.NavbarBrand("United States Power Plant Carbon Dioxide Emissions",
                               className='header-text'
                                )
                    )
                ],
                align = "center",
                style={'margin-bottom': '5px'}
                ),
            ])
    return header

