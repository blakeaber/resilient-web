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
    time
    )


pain_level = dbc.FormGroup(
    [
        dbc.Label("Current Pain Level", html_for="pain-slider"),
        dcc.Slider(
            id="pain-slider", 
            min=0, 
            max=10, 
            step=1, 
            marks={
                0: 'No Pain',
                2: 'Mild',
                4: 'Moderate',
                6: 'Severe',
                8: 'Very Severe',
                10: 'Worst Pain Possible'
            }
        ),
    ]
)


experience = dbc.Card([
    dbc.CardHeader("Pain Diary"),
    dbc.CardBody([
		dbc.Form([pain_level])
        html.H1([
            dbc.Badge(id='pain-display', pill=True, color="success", className="ml-1")
        ], style={'text-align': 'center'}),
    ])
], color="light", outline=True)



layout = dbc.Container([
    dbc.Row([
        dbc.Col(experience, width=12)   
        dbc.Col([
            dbc.Button("Submit", id='profile-submit-button', color="primary", block=True)
            ], 
            width=12),
    ], justify="center")
])


@app.callback(Output('pain-display', 'children'),
              [Input('pain-slider', 'value')])
def disable_tabs_while_recording(value):
    if value:
        return value

