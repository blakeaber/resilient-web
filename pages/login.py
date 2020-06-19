from app import (
    app, 
    dbc, 
    dcc, 
    html, 
    Input, 
    Output, 
    State,
    ClientsideFunction,
    sql,
    time,
    json,
    hashlib
    )


def generate_password_for_user(username, salt):
    salted = username + salt
    md5 = hashlib.md5(salted.encode('utf-8'))
    hashed = md5.hexdigest()
    return hashed[-8:]


login_form = html.Form([
    dbc.FormGroup([
        dcc.Input(type="email", id="login_email", placeholder="Email address")
    ]),
    dbc.FormGroup([
        dcc.Input(type="password", id="login_password", placeholder="Password"),
    ]),
    dbc.Button("Sign In", id='login-button', color="primary")
], className="col-md-5 p-lg-5 mx-auto")


layout = dbc.Jumbotron([
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
        fluid=False
    )],
    fluid=True,
    className="text-center"
)


@app.callback([Output('login-button', 'disabled'), 
               Output('login-button', 'color')],
              [Input('url', 'pathname'),
               Input('login_email', 'value'),
               Input('login_password', 'value')])
def verify_login(pathname, email, password):
    if email and password:
        expected_password = generate_password_for_user(email, 'resilient')
        if password == expected_password:
            return False, 'success'

    return True, 'light'


@app.callback(Output('user-id', 'data'),
              [Input('login-button', 'n_clicks')],
              [State('login_email', 'value'),
               State('login_password', 'value')])
def verify_login(n_clicks, email, password):

    def profile_exists(user_hash):
		sql_statement = f"""
		   SELECT COUNT(profile_id) FROM profiles
		   WHERE user_hash = '{user_hash}'
		   """
		result = sql.select(sql_statement)[0][0]
		return True if result else False

    if n_clicks:
        has_profile = profile_exists(password)
        return {'email': email, 'user-hash': password, 'user-profile-exists': has_profile}
    else:
        return {'email': None, 'user-hash': None}


