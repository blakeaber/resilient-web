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


pain_areas = [
    'Neck',
    'Shoulders',
    'Wrists',
    'Back',
    'Hips',
    'Legs',
    'Knees',
    'Feet'
]


pain_level = dbc.FormGroup(
    [
        dbc.Label("What Is Your Current Pain Level?", html_for="pain-slider"),
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


pain_increase_checklist = dbc.FormGroup(
    [
        dbc.Label("Anything Getting Worse?", html_for="pain-increase-checklist"),
        dbc.Checklist(
            id="pain-increase-checklist",
            options=[
                {"label": i, "value": idx} for idx, i in enumerate(pain_areas)
            ],
            switch=True,
            inline=False
        )
    ]
)


pain_decrease_checklist = dbc.FormGroup(
    [
        dbc.Label("Anything Getting Better?", html_for="pain-decrease-checklist"),
        dbc.Checklist(
            id="pain-decrease-checklist",
            options=[
                {"label": i, "value": idx} for idx, i in enumerate(pain_areas)
            ],
            switch=True,
            inline=False
            
        )
    ]
)


experience = dbc.Card([
    dbc.CardHeader("Pain Diary"),
    dbc.CardBody([
        html.H1([
            dbc.Badge(id='pain-display', pill=True, color="success", className="ml-1")
        ], style={'text-align': 'center'}),
		dbc.Form([
		    pain_level
		])
    ])
], color="light", outline=True)



layout = dbc.Container([
    dbc.Row([
        dbc.Col(experience, width=12),
    ], justify="center"),
    dbc.Row([
        dbc.Col(pain_increase_checklist, width=6),
        dbc.Col(pain_decrease_checklist, width=6)
    ], justify="center"),
    dbc.Row([    
        dbc.Col([
            dbc.Button("Submit", id='diary-submit-button', color="primary", block=True)
        ], 
        width=12),
    ], justify="center"),
])


@app.callback(Output('pain-display', 'children'),
              [Input('pain-slider', 'value')])
def disable_tabs_while_recording(value):
    if value:
        return value

