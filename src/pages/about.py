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
from datetime import datetime
import dash_table
import plotly.graph_objects as go

from .home import get_sidebar


def layout():
    banner = dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(src='./static/brianasamoah.jpeg', alt='Brian Asamoah', className="banner-image"),
                html.Div([
                    html.Span([html.I('Brian Asamoah')]),
                ], className='alt-text'),
                html.Div([
                    html.H1("About"),
                ], className='overlay-text')
            ], className='banner-container')
        ]),
    ])



    layout = [
        get_sidebar(__name__),
        html.Div([
            dbc.Container(banner, fluid=True),
            html.Div(html.H2(f"Website by William Roten", style={'textAlign': 'center'}), className='text-justify'),
            html.Div([
            html.H3([
                "This Website was developed using python and the ",
                dcc.Link('Plotly Dash Library.', href='https://plotly.com/', target='_blank')
            ], style={'textAlign': 'center'})
        ], className='text-justify'),
            html.Div([
                html.H3([
                    "All data was provided by ",
                    dcc.Link('collegefootballdata.com', href='https://collegefootballdata.com/', target='_blank'),
                    " using their API and ",
                    dcc.Link('CFBD Python Library.', href='https://github.com/CFBD/cfbd-python/tree/master', target='_blank') 
                ], style={'textAlign': 'center'})
            ], className='text-justify'),
        ], className='content')
    ]

    return layout