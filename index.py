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
    ClientsideFunction,
    server,
    sql
)
from pages import login, howitworks, profile, diary, exercise, utils
from onboarding import steps


navbar = dbc.NavbarSimple(
    id='nav-bar-id',
    children=[
        dbc.NavLink("Exercises", href="/exercise"),
        dbc.NavLink("Pain Diary", href="/diary"),
        dbc.NavLink("Profile", href="/profile")
    ],
    brand="Resilient.ai",
    brand_href="/",
    color="light",
    dark=False,
    sticky='top',
    style={'display': 'none'}
)


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='user-id', storage_type='memory'),
    navbar,
    html.Div(id='page-content'),
    html.Div(id='start-button-target'),
    html.Div(id='stop-button-target'),
])


def is_valid_user(user):
    if user and user.get('email'):
        return True
    return False

def user_has_profile(user):
    if not is_valid_user(user):
        return False

    user_hash = user.get('user-hash')
    sql_statement = f"""
       SELECT COUNT(profile_id) FROM profiles
       WHERE user_hash = '{user_hash}'
       """
    result = sql.select(sql_statement)[0][0]
    if result:
        return True
    
    return False


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname'),
               Input('user-id', 'data')])
def display_page(pathname, user):

    if not is_valid_user(user):
        return login.layout
    elif not user_has_profile(user):
        return steps.layout        
    elif pathname == '/':
        return exercise.layout
    elif pathname == '/exercise':
        return exercise.layout
    elif pathname == '/diary':
        return diary.layout
    elif pathname == '/profile':
        return profile.layout
    else:
        return '404'


@app.callback(Output('nav-bar-id', 'style'),
              [Input('user-id', 'data'),
               Input('url', 'pathname')])
def display_page(user, pathname):
    if not is_valid_user(user) or not user_has_profile(user):
        return {'display': 'none'}
    else:
        return {'display': 'block'}


if __name__ == '__main__':
    app.run_server(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
