from app import app, dbc, dcc, html, Input, Output, State

card_content_1 = [
    dbc.CardHeader("Instructions"),
    dbc.CardBody([
		html.Iframe(
			id='instruction-video', 
			src='https://www.youtube.com/embed/k3Zi5AYbYU4',
			width=600,
			height=400
		)
	])
]

card_content_2 = [
    dbc.CardHeader("Objectives"),
    dbc.CardBody([
		html.H5("Watch Out For", className="card-title"),
		dbc.ListGroup(
			[
				dbc.ListGroupItem("Straight Arms"),
				dbc.ListGroupItem("Straight Knees"),
				dbc.ListGroupItem("Heels On Floor"),
			],
			flush=True,
		)
	])
]

card_content_3 = [
    dbc.CardHeader("Performance"),
    dbc.CardBody([
		html.H5("Overall", className="card-title"),
		dbc.Progress(value=76, color='light'),
		html.Span([
		    dbc.Button([
		        "Grade", 
		        dbc.Badge("B", pill=True, color="success", className="ml-1"),
			]),
		    dbc.Button([
		        "Form", 
		        dbc.Badge("C", pill=True, color="warning", className="ml-1"),
			]),
		    dbc.Button([
		        "Severity", 
		        dbc.Badge("D", pill=True, color="danger", className="ml-1"),
			])
		])
	])
]

card_1 = dbc.Card(card_content_1, color="light", outline=True)
card_2 = dbc.Card(card_content_2, color="light", outline=True)
card_3 = dbc.Card(card_content_3, color="light", outline=True)

cards = html.Div([
    dbc.Row([
        dbc.Col(card_1, width=8), 
        dbc.Col([
            card_2,
            html.Br(),
            card_3
        ], width=4)
    ])
])


typeform_iframe = html.Iframe(
	id='give-feedback', 
	src='https://ba881.typeform.com/to/hJ6vPg',
	width='100%',
	height=400
)

modal = html.Div(
    [
        dbc.Button("Give Feedback", id="open", color='primary'),
        dbc.Modal(
            [
                dbc.ModalHeader("Quick Survey", style={'float': 'left'}),
                dbc.ModalBody(typeform_iframe),
                dbc.ModalFooter(dbc.Button("Close", id="close", style={'float': 'right'}))
            ],
            id="modal",
            size='xl',
            backdrop='static',
            centered=True
        ),
    ]
)

layout = dbc.Jumbotron([
	cards, 
	modal
])


@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), 
    Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
