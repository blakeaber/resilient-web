from app import app, dbc, dcc, html, Input, Output, State


jumbotron = dbc.Jumbotron([
	dbc.Container([
		html.Iframe(
			id='instruction-video', 
			src='https://www.youtube.com/embed/k3Zi5AYbYU4',
			width=500,
			height=350
		)], 
		fluid=True)], 
	fluid=True
)

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

layout = html.Div([
    jumbotron,
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
