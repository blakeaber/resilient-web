from app import (
    os,
    time,
    app, 
    dash, 
    dbc, 
    dcc, 
    html, 
    Input,
    Output,
    State,
    MATCH,
    ALL,
    ClientsideFunction
)
from pages import howitworks, programs, movement, utils


navbar = dbc.NavbarSimple(
    id='nav-bar-id',
    children=[
        dbc.NavLink("How It Works", href="/howitworks"),
        dbc.NavLink("Programs", href="/programs")
    ],
    brand="Resilient.ai",
    brand_href="/",
    color="light",
    dark=False,
    sticky='top',
    style={'display': 'none'}
)

login_form = html.Form([
    dbc.FormGroup([
        dcc.Input(type="email", id="inputEmail", placeholder="Email address")
    ]),
    dbc.FormGroup([
        dcc.Input(type="password", id="inputPassword", placeholder="Password"),
    ]),
    dbc.Button("Sign In", id='login-button', color="primary")
], className="col-md-5 p-lg-5 mx-auto")

login_page = dbc.Jumbotron([
    dbc.Container(
		[
			html.H1("Friends & Family", className="cover-heading"),
			html.P(
				"We are building a "
				"musculoskeletal wellness platform.",
				className="lead",
			),
			html.P(
				"Please try it out, "
				"and let us know what you think!",
				className="lead",
			),
			login_form
		],
		fluid=True
	)],
    fluid=True,
    className="text-center"
)


recording_modal = dbc.Modal([
        dbc.ModalHeader("Awesome pose estimation AI!"),
        dbc.ModalBody([
            dbc.Button("Start Recording", id="btn-start-recording"),
            dbc.Button("Stop Recording", id="btn-stop-recording"),
            html.Video(id='feedback-video', autoPlay=True, controls=False),
            html.P(id='percentage')
        ]),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-modal-ai")
        ),
    ],
    id="video-modal-ai",
    size="xl"
)


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='user-id', storage_type='local'),
    navbar,
    recording_modal,
    dcc.Loading(
		id="loading-placeholder",
		children=html.Div(login_page, id='page-content'),
		type="circle"
	),
	html.Div(id='start-button-target'),
    html.Div(id='stop-button-target')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname'),
               Input('user-id', 'data')])
def display_page(pathname, user):
    user = user or {'email': None}
    if not user['email']:
        return login_page
    elif user and (pathname == '/'):
        return howitworks.layout
    elif pathname == '/howitworks':
        return howitworks.layout
    elif pathname == '/programs':
        return programs.layout
    elif pathname == '/movement':
        return movement.layout
    else:
        return '404'


@app.callback(Output('nav-bar-id', 'style'),
              [Input('user-id', 'data')])
def display_page(user):
    user = user or {'email': None}
    if user['email']:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(Output('user-id', 'data'),
              [Input('login-button', 'n_clicks')],
              [State('inputEmail', 'value'),
               State('inputPassword', 'value')])
def verify_login(n_clicks, email, password):
    if n_clicks and email:
        expected_password = utils.generate_password_for_user(email, 'resilient')
        if password == expected_password:
            return {'email': email}


app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='click_start_button'
    ),
    Output('start-button-target', 'children'),
    [Input('btn-start-recording', 'active')]
)


app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='click_stop_button'
    ),
    Output('stop-button-target', 'children'),
    [Input('btn-stop-recording', 'active')]
)


@app.callback(
    [Output("btn-start-recording", "active"),
     Output("btn-stop-recording", "active")],
    [Input("btn-start-recording", "n_clicks_timestamp"), 
     Input("btn-stop-recording", "n_clicks_timestamp"),
     Input("video-modal-ai", "is_open")]
)
def toggle_active_button(start_button_ts, stop_button_ts, is_open):
    start_button_ts = int(start_button_ts) if start_button_ts else 0
    stop_button_ts = int(stop_button_ts) if stop_button_ts else 0

    some_buttons_clicked = (start_button_ts or stop_button_ts)
    start_button_clicked = start_button_ts > stop_button_ts
    stop_event = (start_button_ts < stop_button_ts) or not is_open
    stop_before_start = (stop_button_ts and not start_button_ts)

    if not some_buttons_clicked:
        return False, False
    elif stop_before_start:
        return False, False
    elif stop_event:
        return False, True
    elif start_button_clicked:
        return True, False


if __name__ == '__main__':
    app.run_server(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
