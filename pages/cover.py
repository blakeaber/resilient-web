from app import dbc, dcc, html


jumbotron = dbc.Jumbotron([
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
		],
		fluid=True
	)],
    fluid=True,
    className="text-center"
)

login_form = html.Form([
    html.H3("Sign In:"),
    dbc.FormGroup([
        dbc.Input(type="email", id="inputEmail", placeholder="Email address")
    ]),
    dbc.FormGroup([
        dbc.Input(type="password", id="inputPassword", placeholder="Password"),
    ]),
    dbc.Button("Get Started", color="primary")
], className="col-md-5 p-lg-5 mx-auto")

layout = html.Div([
    jumbotron,
    login_form
])


