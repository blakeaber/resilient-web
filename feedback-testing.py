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
				daq.LEDDisplay(id='left-lower-arm-angle', color="#FF5E5E", label="Left Lower Arm Angle"),
				daq.LEDDisplay(id='left-upper-arm-angle', color="#FF5E5E", label="Left Upper Arm Angle"),
				daq.LEDDisplay(id='average-arm-angle', color="#FF5E5E", label="Average Arm Angle"),
				daq.LEDDisplay(id='error-arm-angle', color="#FF5E5E", label="Error Arm Angle"),
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
		input_df = utils.transform_keypoint_payload(converted)

		def get_joint_angles(joint1, joint2):
			return input_df.apply(
				lambda row: logic.angle_between_joints(
					row, 
					joint1, 
					joint2
				), 
				axis=1
			)

		left_arm_low = get_joint_angles('leftWrist', 'leftElbow')
		left_arm_high = get_joint_angles('leftElbow', 'leftShoulder')
		arm_values = pd.concat([left_arm_low, left_arm_high])
		mean_arm_angle, std_arm_angle = arm_values.mean(), arm_values.std()

#		 left_leg_low = get_joint_angles('leftAnkle', 'leftKnee')
#		 left_leg_high = get_joint_angles('leftKnee', 'leftHip')
#		 leg_values = pd.concat([left_leg_low, left_leg_high])
#		 mean_leg_angle, std_leg_angle = leg_values.mean(), leg_values.std()
	
		return json.dumps({
			'left-lower-arm-angle': get_joint_angles('leftWrist', 'leftElbow').mean(),
			'left-upper-arm-angle': get_joint_angles('leftElbow', 'leftShoulder').mean(),
			'average-arm-angle': mean_arm_angle,
			'error-arm-angle': std_arm_angle
#			 'left-lower-leg-angle': get_joint_angles('leftAnkle', 'leftKnee').mean(),
#			 'left-upper-leg-angle': get_joint_angles('leftKnee', 'leftHip').mean(),
#			 'average-leg-angle': mean_leg_angle,
#			 'error-leg-angle': std_leg_angle
		})

@app.callback(
	dash.dependencies.Output('left-lower-arm-angle', 'value'),
	[dash.dependencies.Input('metrics', 'children')])
def update_output(data):
	if data:
		converted = json.loads(data)
		return round(converted['left-lower-arm-angle'], 0)

@app.callback(
	dash.dependencies.Output('left-upper-arm-angle', 'value'),
	[dash.dependencies.Input('metrics', 'children')])
def update_output(data):
	if data:
		converted = json.loads(data)
		return round(converted['left-upper-arm-angle'], 0)

@app.callback(
	dash.dependencies.Output('average-arm-angle', 'value'),
	[dash.dependencies.Input('metrics', 'children')])
def update_output(data):
	if data:
		converted = json.loads(data)
		return round(converted['average-arm-angle'], 0)

@app.callback(
	dash.dependencies.Output('error-arm-angle', 'value'),
	[dash.dependencies.Input('metrics', 'children')])
def update_output(data):
	if data:
		converted = json.loads(data)
		return round(converted['error-arm-angle'], 0)


if __name__ == '__main__':
	app.run_server(host='127.0.0.1', debug=True)
