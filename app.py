import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH, ALL

import os


# external JavaScript files
external_scripts = [
    'https://cdn.jsdelivr.net/npm/@tensorflow/tfjs',
    'https://cdn.jsdelivr.net/npm/@tensorflow-models/posenet',
	'https://cdn.jsdelivr.net/npm/uikit@3.4.0/dist/js/uikit.min.js',
	'https://cdn.jsdelivr.net/npm/uikit@3.4.0/dist/js/uikit-icons.min.js'
]


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
