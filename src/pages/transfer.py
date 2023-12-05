import dash
import json
import dash_bootstrap_components as dbc
from dash import html, ctx, Input, Output, State, clientside_callback, dcc
import dash_bootstrap_components as dbc
import time
import cfbd
from cfbd.rest import ApiException
import pandas as pd
from dash import dash_table
from dash.dependencies import Input, Output
from dash import Dash
import json
import datetime
import dash_table
import plotly.graph_objects as go

from .home import get_sidebar

configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = '1xI15NQRMSZbOe+ZSYPCVPy7lqqBixpoV+jo/FGxOEm8MjBfoIfCvX0aN4YA+bhk'
configuration.api_key_prefix['Authorization'] = 'Bearer'

def fetch_recruiting_data():
    api_instance = cfbd.PlayersApi(cfbd.ApiClient(configuration))

    year = 2023 # str | Committed team filter (required if year not specified) (optional)

    transfers = api_instance.get_transfer_portal(year=year)
    
    
        
        # Convert each Game object to a dictionary
    transfers = [transfer.to_dict() for transfer in transfers]
    transfers

    # Your dictionary
    # Convert dictionary to DataFrame
    transfersdf = pd.DataFrame(transfers)
    transfersdf.sort_values('rating', ascending=False, inplace=True)
    transfersdf['transfer_date'] = pd.to_datetime(transfersdf['transfer_date']).dt.strftime('%m-%d-%Y')
    transfersdf = transfersdf.drop(columns="season")
    transfersdf = transfersdf.rename(columns={
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'position': 'Position',
        'origin': 'Origin School',
        'destination': 'Destination School',
        'transfer_date': 'Transfer Date',
        'rating': 'Rating',
        'stars': 'Stars',
        'eligibility': 'Eligibility',
        
    })
    transfersdf['Destination School'] = transfersdf['Destination School'].fillna('Undecided')
    transfersdf['Transfer Date'] = pd.to_datetime(transfersdf['Transfer Date'])
    
    return transfersdf


def layout():
    banner = dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(src='./static/sambradford.jpg', alt='kyler', className="banner-image"),
                html.Div([
                    html.Span([html.I('Sam Bradford')]),
                ], className='alt-text'),
                html.Div([
                    html.H1("Transfer Portal"),
                ], className='overlay-text')
            ], className='banner-container')
        ]),
    ])

    
    transfers = fetch_recruiting_data()

    # Create a DataTable from the transfers data
    transfers_table = dash_table.DataTable(
        id='transfers_table',
        columns=[{"name": i, "id": i} for i in transfers.columns],
        data=transfers.to_dict('records'),
        style_table={'overflowX': 'auto'},
        filter_action='native',  # enable built-in filtering
        style_data={  # add a border around the table
            'border': '1px solid black'
        },
        sort_action='native'  # enable built-in sorting
    )

    # Your existing layout code...
    layout = [
        get_sidebar(__name__),
        html.Div([
            dbc.Container(banner, fluid=True),
            html.Div(html.H1(f"Transfer Portal", style={'textAlign': 'center', 'fontWeight': 'bold'}), className='text-justify'),
            dbc.Container(dbc.Row(dbc.Col(transfers_table)), fluid='md')  # add the transfers table to the layout
        ], className='content')
    ]

    return layout