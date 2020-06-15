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
    server
)
from pages import login, howitworks, profile, diary, exercise, utils
from onboarding import steps


navbar = dbc.NavbarSimple(
    id='nav-bar-id',
    children=[
        dbc.NavLink("How It Works", href="/howitworks"),
        dbc.NavLink("Profile", href="/profile"),
        dbc.NavLink("Diary", href="/diary"),
        dbc.NavLink("Exercises", href="/exercise")
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


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname'),
               Input('user-id', 'data')])
def display_page(pathname, user):
    if not user or not user.get('email'):
        return login.layout
    elif user and (pathname == '/'):
        return profile.layout
    elif pathname == '/howitworks':
        return howitworks.layout
    elif pathname == '/onboard':
        return steps.layout
    elif pathname == '/exercise':
        return exercise.layout
    elif pathname == '/profile':
        return profile.layout
    elif pathname == '/diary':
        return diary.layout
    else:
        return '404'


@app.callback(Output('nav-bar-id', 'style'),
              [Input('user-id', 'data')])
def display_page(user):
    if not user or not user.get('email'):
        return {'display': 'none'}
    else:
        return {'display': 'block'}


if __name__ == '__main__':
    app.run_server(
#         host='0.0.0.0',
        host='localhost',
        port=5000,
        debug=True
    )
