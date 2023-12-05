import json
import dash_bootstrap_components as dbc
from dash import html
import time
import cfbd
from cfbd.rest import ApiException
import pandas as pd
from datetime import datetime

def get_sidebar(active_item=None):
    nav = html.Nav(id="sidebar", className="active", children=[
        html.Div(className="custom-menu", children=[
            html.Button([
                html.I(className="fa fa-bars"),
                html.Span("Toggle Menu", className="sr-only")
            ], type="button", id="sidebarCollapse", className="btn btn-primary")
        ]),
        html.Div(className="flex-column p-4 nav nav-pills", children=[
            html.A([
                html.Img(src='./static/nav.png', alt='', width=48, height=48, className='mx-2'),
                html.Span("Sooner Stats", className='fs-4'),
            ], className='d-flex align-items-center mb-3 mb-md-0 me-md-auto text-white text-decoration-none', href='/'),
            html.Hr(),
            dbc.NavItem(dbc.NavLink("Home", href="/", className='text-white', active=True if active_item=='pages.home' else False)),
            dbc.NavItem(dbc.NavLink("Games", href="/games", className='text-white', active=True if active_item=='pages.games' else False)),
            dbc.NavItem(dbc.NavLink("Players", href="/players", className='text-white', active=True if active_item=='pages.players' else False)),
            dbc.NavItem(dbc.NavLink("Recruiting", href="/recruiting", className='text-white', active=True if active_item=='pages.recruiting' else False)),
            dbc.NavItem(dbc.NavLink("Transfer Portal", href="/transfer", className='text-white', active=True if active_item=='pages.transfer' else False)),
            dbc.NavItem(dbc.NavLink("About", href="/about", className='text-white', active=True if active_item=='pages.about' else False)),
        ])
    ])
    return nav

configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = '1xI15NQRMSZbOe+ZSYPCVPy7lqqBixpoV+jo/FGxOEm8MjBfoIfCvX0aN4YA+bhk'
configuration.api_key_prefix['Authorization'] = 'Bearer'

def calculate_win_percentage(record):
    wins, losses = map(int, record.split('-'))
    total_games = wins + losses
    return round((wins / total_games) * 100, 2) if total_games > 0 else 0

def update_team_stats():


    api_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))
    year = datetime.now().year
    team = 'Oklahoma'

    
    api_response = api_instance.get_team_records(year = year, team = team)   

    def convert_record_to_single_value(record):
        return f"{record['wins']}-{record['losses']}"

    api_response_dict = [obj.to_dict() for obj in api_response]

    for record in api_response_dict:
        record['total'] = convert_record_to_single_value(record['total'])
        record['conference_games'] = convert_record_to_single_value(record['conference_games'])
        record['home_games'] = convert_record_to_single_value(record['home_games'])
        record['away_games'] = convert_record_to_single_value(record['away_games'])
    team_stats = pd.DataFrame(api_response_dict)

    team_stats = team_stats.rename(columns={
        'total': 'Overall_Record',
        'conference_games': 'Conference_Record',
        'home_games': 'Home_Record',
        'away_games': 'Away_Record'
    })

    return team_stats

def generate_cards(team_stats):
    cards = []

    for index, row in team_stats.iterrows():
        for stat_name in ['Overall_Record', 'Conference_Record', 'Home_Record', 'Away_Record']:
            win_percentage = calculate_win_percentage(row[stat_name])
            card_content = [
                dbc.CardHeader(stat_name.capitalize().replace('_', ' '), className="text-center"),
                dbc.CardBody(
                    [
                        html.H5(f"{row[stat_name]} ({win_percentage}%)", className="card-title text-center"),
                    ]
                ),
            ]
            card = dbc.Card(card_content, className="mb-3", style={"borderRadius": "15px"})
            cards.append(dbc.Card(card_content, className="mb-3", style={"borderRadius": "15px"}))

    return cards

team_stats = update_team_stats()
cards = generate_cards(team_stats)

def layout():
    banner = dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(src='./static/bakerplantingflag.jpg', alt='baker mayfield', className="banner-image"),
                html.Div([
                    html.Span([html.I('Baker Mayfield')]),
                    
                ], className='alt-text'),
                html.Div([
                    html.H2("Sooner Stats"),
                    html.P("Welcome to SoonerStats.Com, a website dedicated to the Oklahoma Sooners Football Team.")
                ], className='overlay-text')
            ], className='banner-container')
        ]),
    ])

    layout_components = dbc.Row([
        
            html.Div(html.H1(f"Oklahoma Sooner {datetime.now().year} Season Record", style={'textAlign': 'center', 'fontWeight': 'bold'}), className='text-justify'),
            html.Div(cards),
            html.Div([html.I("Data Provided By")," https://collegefootballdata.com"], className='ref text-end') 
        ,
        
    ], className='mb-4 mt-2 align-items-end', justify= 'center')

    layout = [
        get_sidebar(__name__),
        html.Div([
            dbc.Container(banner, fluid=True),
            dbc.Container(layout_components, fluid='md')
        ], className='content')
    ]

    return layout