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


app = Dash(__name__)

with open('./pages/text.json') as f:
    about = json.load(f)['about']

def get_description():
    return "Test"

configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = '1xI15NQRMSZbOe+ZSYPCVPy7lqqBixpoV+jo/FGxOEm8MjBfoIfCvX0aN4YA+bhk'
configuration.api_key_prefix['Authorization'] = 'Bearer'



def fetch_game_data():
    api_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))
    year = 2023
    team = 'Oklahoma'
    season_type = 'both'

    games = api_instance.get_games(year=year, team=team, season_type=season_type)
    
        
        # Convert each Game object to a dictionary
    games = [game.to_dict() for game in games]
    games

    # Your dictionary
    # Convert dictionary to DataFrame
    gamesdf = pd.DataFrame(games)
    gamesdf

    api_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))
    year = 2023
    team = 'Oklahoma'


    games = api_instance.get_team_game_stats(year=year, team=team)
    api_response_dict = [obj.to_dict() for obj in games]
    df = pd.DataFrame(api_response_dict)
    # Assuming you already have the 'df' DataFrame
    df_teams = pd.json_normalize(df['teams'])

    # Concatenate the 'df' DataFrame with the 'df_teams' DataFrame
    df = pd.concat([df, df_teams], axis=1)

    # Drop the 'teams' column
    df = df.drop('teams', axis=1)
    df = df.rename(columns={0: 'Home', 1: 'Away'})

    # Extract the stats from the 'Home' column
    df_home_stats = pd.json_normalize(df['Home'])
    df_home_stats.columns = ['Home ' + col for col in df_home_stats.columns]

    # Extract the stats from the 'Away' column
    df_away_stats = pd.json_normalize(df['Away'])
    df_away_stats.columns = ['Away ' + col for col in df_away_stats.columns]

    # Concatenate the 'df' DataFrame with the 'df_home_stats' and 'df_away_stats' DataFrames
    df = pd.concat([df, df_home_stats, df_away_stats], axis=1)

    # Drop the 'Home' and 'Away' columns
    df = df.drop(['Home', 'Away'], axis=1)

    df_home_stats = df['Home stats'].apply(lambda x: {item['category']: item['stat'] for item in x}).apply(pd.Series)
    df_away_stats = df['Away stats'].apply(lambda x: {item['category']: item['stat'] for item in x}).apply(pd.Series)

    # Add the data back to the original DataFrame
    df = pd.concat([df, df_home_stats.add_prefix('Home_'), df_away_stats.add_prefix('Away_')], axis=1)
    df = df.drop(['Home stats', 'Away stats'], axis=1)
    gamesdf = gamesdf.merge(df, on='id', how='left')
    gamesdf = gamesdf.sort_values('id')
    

    return gamesdf

game_data = fetch_game_data()



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def layout():
    banner = dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(src='./static/stadium.jpg', alt='baker', className="banner-image"),
                html.Div([
                    html.Span([html.I('Red River Rivalry')]),
                ], className='alt-text'),
                html.Div([
                    html.H1("Game Breakdown"),
                ], className='overlay-text')
            ], className='banner-container')
        ]),
    ])

    game_data_dicts = game_data.to_dict('records')
    
    # Define the columns to keep and their new names
    # Define the columns to keep and their new names
    columns_to_keep = ['home_team', 'away_team', 'home_points', 'away_points', 'venue', 'start_date', 
                    'Home_rushingTDs', 'Home_passingTDs', 'Home_kickReturnYards', 'Home_kickReturnTDs', 
                    'Home_kickReturns', 'Home_kickingPoints', 'Home_fumblesRecovered', 'Home_totalFumbles', 
                    'Home_tacklesForLoss', 'Home_defensiveTDs', 'Home_tackles', 'Home_sacks', 'Home_qbHurries', 
                    'Home_passesDeflected', 'Home_possessionTime', 'Home_interceptions', 'Home_fumblesLost', 
                    'Home_turnovers', 'Home_totalPenaltiesYards', 'Home_yardsPerRushAttempt', 'Home_rushingAttempts', 
                    'Home_rushingYards', 'Home_yardsPerPass', 'Home_completionAttempts', 'Home_netPassingYards', 
                    'Home_totalYards', 'Home_fourthDownEff', 'Home_thirdDownEff', 'Home_firstDowns']

    new_column_names = ['Home Team', 'Away Team', 'Home Score', 'Away Score', 'Venue', 'Date', 
                    'Home Rushing TDs', 'Home Passing TDs', 'Home Kick Return Yards', 'Home Kick Return TDs', 
                    'Home Kick Returns', 'Home Kicking Points', 'Home Fumbles Recovered', 'Home Total Fumbles', 
                    'Home Tackles For Loss', 'Home Defensive TDs', 'Home Tackles', 'Home Sacks', 'Home QB Hurries', 
                    'Home Passes Deflected', 'Home Possession Time', 'Home Interceptions', 'Home Fumbles Lost', 
                    'Home Turnovers', 'Home Total Penalties Yards', 'Home Yards Per Rush Attempt', 'Home Rushing Attempts', 
                    'Home Rushing Yards', 'Home Yards Per Pass', 'Home Completion Attempts', 'Home Net Passing Yards', 
                    'Home Total Yards', 'Home Fourth Down Efficiency', 'Home Third Down Efficiency', 'Home First Downs']
    
    # Filter and rename the columns
    filtered_game_data = game_data[columns_to_keep]
    filtered_game_data.columns = new_column_names

    # Convert the 'Date' column to datetime and format it
    filtered_game_data['Date'] = pd.to_datetime(filtered_game_data['Date'])
    filtered_game_data['Date'] = filtered_game_data['Date'].dt.strftime('%B %d, %Y')

    table = dbc.Table.from_dataframe(filtered_game_data, striped=True, bordered=True, hover=True)
    html.Div(" ", style={'padding': '10px'})
    scrollable_table = html.Div(table, style={'overflowX': 'auto'})


    table_card = dbc.Card(
        [
            html.H2(f"{datetime.now().year} Oklahoma Sooners Game Data", style={'textAlign': 'center', 'fontWeight': 'bold'}),  # Centered, larger, bold title
            dbc.CardBody(scrollable_table),
        ],
        className="mb-3",
        style={'padding': '10px'}  # Add padding around the card
)

    layout = [
        get_sidebar(__name__),
        html.Div([
            dbc.Container(banner, fluid=True),
            dbc.Container(table_card),  # Use the Card here
            
        ], className='content')
    ]

    return layout

clientside_callback(
    """
    function(yes, name){
        if (name === 'active') {
            return '';
        } else if (name === '') {
            return 'active';
        }
    }
    """,
    Output('sidebar', 'className'),
    Input('sidebarCollapse', 'n_clicks'),
    State('sidebar', 'className')
)


