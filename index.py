from app import (
    os,
    app, 
    dash, 
    dbc, 
    dcc, 
    html, 
    flask,
    Input,
    Output,
    State
)
from pages import demo, cover, exercises, movement


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavLink("Exercises", href="/exercises"),
        dbc.NavLink("Movement", href="/movement"),
    ],
    brand="Resilient.ai",
    color="light",
    dark=False,
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return cover.layout
    elif pathname == '/exercises':
        return exercises.layout
    elif pathname == '/movement':
        return movement.layout
    else:
        return '404'


if __name__ == '__main__':
    debug = False if os.environ['DASH_DEBUG_MODE'] == 'False' else True

    app.run_server(
        host='0.0.0.0',
        port=5000,
        debug=debug
    )
