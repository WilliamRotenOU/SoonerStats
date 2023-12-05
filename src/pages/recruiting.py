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
    api_instance = cfbd.RecruitingApi(cfbd.ApiClient(configuration))

    team = 'oklahoma' # str | Committed team filter (required if year not specified) (optional)


    recruits = api_instance.get_recruiting_players(team=team)
        
            
            # Convert each Game object to a dictionary
    recruits = [recruit.to_dict() for recruit in recruits]
    recruits

        # Your dictionary
        # Convert dictionary to DataFrame
    recruitsdf = pd.DataFrame(recruits)
    current_year = datetime.datetime.now().year
    recruitsdf = recruitsdf[recruitsdf['year'] >= current_year]
    recruitsdf = recruitsdf.drop(['id', 'athlete_id', 'hometown_info', 'committed_to'], axis=1)

    recruitsdf = recruitsdf.rename(columns={
        'recruit_type': 'Recruit Type',
        'year': 'Year',
        'ranking': 'Ranking',
        'name': 'Name',
        'school': 'School',
        'position': 'Position',
        'height': 'Height',
        'weight': 'Weight',
        'stars': 'Stars',
        'rating': 'Rating',
        'city': 'City',
        'state_province': 'State',
        'country': 'Country',
        # Add more columns as needed
    })

    return recruitsdf



def layout():
    banner = dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(src='./static/kylermurray.jpg', alt='kyler', className="banner-image"),
                html.Div([
                    html.Span([html.I('Kyler Murray')]),
                ], className='alt-text'),
                html.Div([
                    html.H1("Recruits"),
                ], className='overlay-text')
            ], className='banner-container')
        ]),
    ])
    recruiting_data = fetch_recruiting_data()
    
    # Create a Table trace from the recruiting data
    trace = go.Table(
        header=dict(values=recruiting_data.columns.tolist(), fill_color='#841617', align='center', font=dict(color='white')),
        cells=dict(values=[recruiting_data[col].tolist() for col in recruiting_data.columns], fill_color='#efe5c7', align='left'),
        columnwidth=[1.2, 1, 1, 3, 3,1,1,1,1,1,1.5,1,1]
    )

    # Create a Graph from the Table trace
    graph = dcc.Graph(
        id='recruit_graph',
        figure=go.Figure(
            data=[trace],
            layout=go.Layout(
                autosize=True,
                height=800  # adjust this value to change the number of visible rows
            )
        )
    )
    
    layout = [
        get_sidebar(__name__),
        html.Div([
            dbc.Container(banner, fluid=True),
            html.Div(html.H1(f"Oklahoma Sooner Commits", style={'textAlign': 'center', 'fontWeight': 'bold'}), className='text-justify'),
            dbc.Row(dbc.Col(graph))  # add the graph to the layout
        ], className='content')
    ]

    return layout