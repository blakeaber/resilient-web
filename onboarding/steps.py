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
    json
    )
from pages import profile, diary, exercise


INPUT_STEPS = [
    'Welcome',
    'Health Profile',
    'Pain Assessment',
    'Exercise Program'
]


def create_process_steps_from_list(input_steps):
    total_steps = len(input_steps)
    if (total_steps > 12) or (total_steps < 1):
        return ValueError('Number of steps must be 1 <= steps <= 12!')

    step_width = 12 / total_steps
    return [
        dbc.Tab(
            tab_id=step_idx+1,
            label=step_text,
            label_style={
                'border': 'none',
                'border-color': 'none',
                'margin': '0 auto'
            },
            tab_style={'margin': '0 auto'}
        ) for step_idx, step_text in enumerate(input_steps)
    ]


welcome = html.P('Welcome!!!')


layout = dbc.Container([
    html.Br(),
    dbc.Tabs(id='onboarding-steps', children=create_process_steps_from_list(INPUT_STEPS)),
    dbc.Row([
        dbc.Col(dbc.Progress(
            id='progress-steps', 
            max=90, 
            color='primary', 
            striped=True, 
            animated=True
        ))
    ]),
    html.Br(),
    html.Div(id='onboarding-content'),
])


@app.callback([Output('onboarding-content', 'children'),
               Output('progress-steps', 'value')],
              [Input('onboarding-steps', 'active_tab')])
def display_page(active_tab):
    if not active_tab or (active_tab == 1):
        return welcome, 15
    elif active_tab == 2:
        return profile.layout, 30
    elif active_tab == 3:
        return diary.layout, 50
    elif active_tab == 4:
        return welcome, 80
#         return exercise.layout
    else:
        return html.P('This indicates an error has occured :(')


