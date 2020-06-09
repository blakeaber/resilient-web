from app import (
    app, 
    dbc, 
    dcc, 
    html, 
    Input, 
    Output, 
    State,
    ClientsideFunction,
    sql
    )
from pages import utils


exercises = dbc.Card(
    dbc.CardHeader([
        dbc.Tabs(
            [
                dbc.Tab(id='exercise-tab-1', label="1. Couch Stretch", tab_id=1),
                dbc.Tab(id='exercise-tab-2', label="2. Inch Worm", tab_id=7),    
                dbc.Tab(id='exercise-tab-3', label="3. Half Kneeling Windmill", tab_id=11)
            ],
            id="exercise-tabs",
            active_tab=1,
            card=True
        )
    ])
, color="light", outline=True)


videos = dbc.Card(
    dbc.CardBody([
        html.Div(
            html.Iframe(id='instructional-video', className='embed-responsive-item'),
            className='embed-responsive embed-responsive-16by9'
        ),
        html.Video(id='feedback-video'),
        html.P(id='percentage')
    ])
, color="light", outline=True)


controls = dbc.Card([
    dbc.CardHeader("Recording"),
    dbc.CardBody([
        dbc.Button("Start", id="btn-start-recording"),
        dbc.Button("Stop", id="btn-stop-recording"),
    ])
], color="light", outline=True)


layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col(exercises, width=12)
            ], justify="center"),
            dbc.Row([
                dbc.Col(videos, width=12)
            ], justify="center"),
        ], width=7), 
        dbc.Col(controls, width=5)
    ], justify="center")
])


@app.callback(Output('instructional-video', 'src'),
              [Input('exercise-tabs', 'active_tab')])
def display_program_movement(active_tab):
    if active_tab == 1:
        return 'https://player.vimeo.com/video/112866269'
    elif active_tab == 7:
        return 'https://player.vimeo.com/video/70591644'
    elif active_tab == 11:
        return 'https://player.vimeo.com/video/347119375'
    else:
        return None


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
     Input("btn-stop-recording", "n_clicks_timestamp")]
)
def toggle_active_button(start_button_ts, stop_button_ts):
    start_button_ts = int(start_button_ts) if start_button_ts else 0
    stop_button_ts = int(stop_button_ts) if stop_button_ts else 0

    some_buttons_clicked = (start_button_ts or stop_button_ts)
    start_button_clicked = start_button_ts > stop_button_ts
    stop_event = (start_button_ts < stop_button_ts)
    stop_before_start = (stop_button_ts and not start_button_ts)

    if not some_buttons_clicked:
        return False, False
    elif stop_before_start:
        return False, False
    elif stop_event:
        return False, True
    elif start_button_clicked:
        return True, False


