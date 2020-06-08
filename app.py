import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH, ALL, ClientsideFunction

import os
import time
from src.sql_model import Sql


# external JavaScript files
external_scripts = [
    'https://cdn.jsdelivr.net/npm/@tensorflow/tfjs',
    'https://cdn.jsdelivr.net/npm/@tensorflow-models/posenet',
	'https://cdn.jsdelivr.net/npm/uikit@3.4.0/dist/js/uikit.min.js',
	'https://cdn.jsdelivr.net/npm/uikit@3.4.0/dist/js/uikit-icons.min.js',
	'https://www.WebRTC-Experiment.com/RecordRTC.js',
	'https://sdk.amazonaws.com/js/aws-sdk-2.1.12.min.js',
	'https://player.vimeo.com/api/player.js',
]


# App Instantiation
app = dash.Dash(
    __name__,
    external_scripts=external_scripts,
    external_stylesheets=[
        dbc.themes.LUX
    ],
    meta_tags=[{
      'name': 'viewport',
      'content': 'width=device-width, initial-scale=1.0'
    }]
)
app.title = 'Resilient.ai ALPHA'
app.config.suppress_callback_exceptions = True

# Gunicorn Invocation
server = app.server

# Postgres Connector
sql = Sql(
    user = os.environ['RDS_USER'],
    password = os.environ['RDS_PASS'],
    host = os.environ['RDS_ENDPOINT'],
    port = os.environ['RDS_PORT'],
    database = "postgres"
)
