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
from .home import get_sidebar
import json
from datetime import datetime

from .home import get_sidebar
configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = '1xI15NQRMSZbOe+ZSYPCVPy7lqqBixpoV+jo/FGxOEm8MjBfoIfCvX0aN4YA+bhk'
configuration.api_key_prefix['Authorization'] = 'Bearer'

with open('pages/text.json') as f:
    about = json.load(f)['about']

def fetch_player_data():
    api_instance = cfbd.PlayersApi(cfbd.ApiClient(configuration))
    year = 2023
    team = 'Oklahoma'
    season_type = 'both'

    playerstats = api_instance.get_player_season_stats(year=year, team=team, season_type=season_type)
        
            

    playerstats

    api_response_dict = [obj.to_dict() for obj in playerstats]
    playersdf = pd.DataFrame(api_response_dict)
        # Sort the DataFrame by 'player_id' in ascending order and remove the 'season' column
    playersdf = playersdf.sort_values('player_id').drop(columns='season')
    playersdf = playersdf.drop(columns="player_id")
    # Remove rows where 'player' is 'Team'
    playersdf = playersdf[playersdf['player'] != ' Team']

    return playersdf

player_data = fetch_player_data()


def layout():
    banner = dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(src='./static/jalenhurts.jpg', alt='baker', className="banner-image"),
                html.Div([
                    html.Span([html.I('Jalen Hurts')]),
                ], className='alt-text'),
                html.Div([
                    html.H1("Player Stats"),
                ], className='overlay-text')
            ], className='banner-container')
        ]),
    ])
    
# Create a DataTable from the player data
    table = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in player_data.columns],
        data=player_data.to_dict('records'),
        filter_action="native",  # allow users to filter the data
        sort_action="native",  # allow users to sort the data
        sort_mode="multi",  # allow users to sort on multiple columns
        column_selectable="single",  # allow users to select columns
        selected_columns=[],  # initialize without any columns selected
        selected_rows=[],  # initialize without any rows selected
        page_action="native",  # enable pagination
        page_current=0,  # start at the first page
        page_size=25,  # number of rows per page
    )

    # Your existing layout code...
    layout = [
        get_sidebar(__name__),
        html.Div([
            dbc.Container(banner, fluid=True),
            html.Div(html.H1(f"{datetime.now().year} Oklahoma Sooner Player Stat Breakdown", style={'textAlign': 'center', 'fontWeight': 'bold'}), className='text-justify'),
            dbc.Container(dbc.Row(dbc.Col(table)), fluid='md')  # add the table to the layout
        ], className='content')
    ]


    return layout
