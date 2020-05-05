import json

import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd
from feedback import utils, logic, inch_worm

# external JavaScript files
external_scripts = [
	'https://cdn.jsdelivr.net/npm/@tensorflow/tfjs',
	'https://cdn.jsdelivr.net/npm/@tensorflow-models/posenet'
]

app = dash.Dash(
	__name__, 
	external_scripts=external_scripts,
	meta_tags=[{
	  'name': 'viewport',
	  'content': 'width=device-width, initial-scale=1.0'
	}]
)
app.title = 'Resilient.ai Demo'


USER_VIDEO = html.Div(
	children=[
		html.Video(id='user-video', autoPlay=True, controls=False)
	]
)

app.layout = html.Div([
	html.Div(
		children=html.Div([
			html.Div(id='info', style={'display': 'none'}),
			html.Div(id='poses', style={'display': 'none'}),
			html.Div([
				daq.BooleanSwitch(id='lower-arm-angle', color="green", label="Arms Straight?"),
				html.Hr(),
				daq.BooleanSwitch(id='lower-leg-angle', color="green", label="Legs Moving?"),
# 				daq.LEDDisplay(id='lower-leg-angle', color="#FF5E5E", label="Leg Angle")
			], style={'float': 'left'}),
			html.Div(USER_VIDEO, style={'float': 'left'}),
			html.Div(id='metrics', style={'display': 'none'})
		])
	),
	dcc.Interval(
		id='interval',
		interval=500, # in milliseconds
		n_intervals=0
	)
])

app.clientside_callback(
	"""
	function () {
		return sessionStorage.getItem('cachePoses');
	}
	""",
	Output('poses', 'children'),
	[Input('interval', 'n_intervals')]
)


@app.callback(Output('metrics', 'children'),
			  [Input('interval', 'n_intervals')],
			  [State('poses', 'children')])
def on_click(n_clicks, data):
	if data:
		converted = json.loads(data)
		input_df = utils.get_df_from_payload(converted)
		input_df = utils.transform_keypoint_payload(input_df)
	
		return json.dumps({
			'lower-arm-angle': inch_worm.lower_arm_down(input_df),
			'lower-leg-angle': inch_worm.lower_leg_angle_achieved(input_df)
		})

@app.callback(
	dash.dependencies.Output('lower-arm-angle', 'on'),
	[dash.dependencies.Input('metrics', 'children')])
def update_output(data):
	if data:
		converted = json.loads(data)
		return converted['lower-arm-angle']

@app.callback(
	dash.dependencies.Output('lower-leg-angle', 'on'),
	[dash.dependencies.Input('metrics', 'children')])
def update_output(data):
	if data:
		converted = json.loads(data)
		return round(converted['lower-leg-angle'], 0)


if __name__ == '__main__':
	app.run_server(host='127.0.0.1', debug=True)
