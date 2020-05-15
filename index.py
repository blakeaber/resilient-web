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
    ALL
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


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='user-id', storage_type='local'),
    navbar,
    dcc.Loading(
		id="loading-placeholder",
		children=html.Div(login_page, id='page-content'),
		type="circle"
	)
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


if __name__ == '__main__':
    debug = False if os.environ['DASH_DEBUG_MODE'] == 'False' else True

    app.run_server(
        host='0.0.0.0',
        port=os.environ['APP_PORT'],
        debug=debug
    )
