from app import app, dbc, dcc, html, Input, Output, State
from pages import data, utils


typeform_iframe = html.Iframe(
	id='give-feedback', 
	src='https://ba881.typeform.com/to/hJ6vPg',
	width='100%',
	height=400
)


modal_feedback = dbc.Modal(
	[
		dbc.ModalHeader("Quick Survey", style={'float': 'left'}),
		dbc.ModalBody(typeform_iframe),
		dbc.ModalFooter(dbc.Button("Close", id="close-modal-feedback", style={'float': 'right'}))
	],
	id="modal-feedback",
	size='xl',
	backdrop='static',
	centered=True
)


feedback_request = dbc.Alert([
	html.P("Honest feedback is the only way we can be successful!"),
	dbc.Button("Give Feedback", id="open-modal-feedback")
	],
	id="feedback-alert",
	color='info',
	is_open=True
)


modal_ai = dbc.Modal(
            [
                dbc.ModalHeader("Awesome pose estimation AI!"),
                dbc.ModalBody("HTML Video, on/off recording buttons, etc"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-modal-ai")
                ),
            ],
            id="video-modal-ai",
            size="xl"
        )


card_content_1 = [
	dbc.CardHeader([
		dbc.Tabs(
			[
				dbc.Tab(label="Movement 1", tab_id="tab-1"),
				dbc.Tab(label="Movement 2", tab_id="tab-2"),
				dbc.Tab(label="Movement 3", tab_id="tab-3")
			],
			id="card-tabs",
			card=True,
			active_tab="tab-1",
		)
	]),
    dbc.CardBody([
        dbc.Alert([
            "After watching the video, try it out with ",
            dbc.Button([
                "digital  ", 
                html.Img(width=50, src='https://static.thenounproject.com/png/2486348-200.png'),
                "  feedback", 
            ], id="open-modal-ai")
            ],
            id="alert-fade",
            color='secondary',
            dismissable=True,
            is_open=True,
        ),
		html.Iframe(
			id='instruction-video',
			width=600,
			height=400
		)
	])
]
card_1 = dbc.Card(card_content_1, color="light", outline=True)


card_content_2 = [
    dbc.CardHeader("Details"),
    dbc.CardBody([
		html.H5("Help Us Improve", className="card-title"),
        feedback_request,
    	modal_feedback
	]),
    dbc.CardBody([
		html.H5("Difficulty", className="card-title"),
        dbc.ButtonGroup([
            dbc.Button("Baseline", active=True), 
            dbc.Button("Advanced")
            ],
            size="sm"
        )]),
    dbc.CardBody([
		html.H5("Watch Out For", className="card-title"),
		dbc.ListGroup(
			id='watch-out-for',
			flush=True,
		)
	])
]
card_2 = dbc.Card(card_content_2, color="light", outline=True)


cards = html.Div([
    dbc.Row([
        dbc.Col(card_1, width=8), 
        dbc.Col(card_2, width=4)
    ])
])


layout = dbc.Container([
	cards,
	modal_ai
	])


@app.callback(Output('instruction-video', 'src'),
              [Input('url', 'href')],
              [State('url', 'pathname')])
def display_instructional_video(href, pathname):
    if pathname.startswith('/movement'):
        exercise = utils.parse_url_parameters(href, param='ex')
        if exercise:
	        return data.EXERCISES[exercise]['video-link']


@app.callback(Output('watch-out-for', 'children'),
              [Input('url', 'href')],
              [State('url', 'pathname')])
def display_instructions(href, pathname):
    if pathname.startswith('/movement'):
        exercise = utils.parse_url_parameters(href, param='ex')
        if exercise:
            return [
                dbc.ListGroupItem(item) for item in data.EXERCISES[exercise]['watch-out-for']
            ]


@app.callback(
    Output("modal-feedback", "is_open"),
    [Input("open-modal-feedback", "n_clicks"), 
    Input("close-modal-feedback", "n_clicks")],
    [State("modal-feedback", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output("video-modal-ai", "is_open"),
    [Input("open-modal-ai", "n_clicks"), Input("close-modal-ai", "n_clicks")],
    [State("video-modal-ai", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
