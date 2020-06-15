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
            min=-1, 
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
                {"label": i, "value": i} for i in pain_areas
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
                {"label": i, "value": i} for i in pain_areas
            ],
            switch=True,
            inline=False
            
        )
    ]
)


experience = dbc.Card([
    dbc.CardHeader("Pain Diary"),
    dbc.CardBody([
		dbc.Form([
		    pain_level
		])
    ])
], color="light", outline=True)



onboard_layout = dbc.Container([
    dbc.Row([
        dbc.Col(experience, width=12),
    ], justify="center"),
    dbc.Row([
        dbc.Col(pain_increase_checklist, width=6),
        dbc.Col(pain_decrease_checklist, width=6)
    ], justify="center")
])


layout = dbc.Container([
    onboard_layout,
    dbc.Row([    
        dbc.Col([
            html.Div(id='diary-submit-status'),
            dbc.Button("Submit", id='diary-submit-button', color="primary", block=True)
        ], 
        width=12),
    ], justify="center"),
])


@app.callback(Output('diary-submit-status', 'children'),
              [Input('diary-submit-button', 'n_clicks')],
              [State('user-id', 'data'),
               State('pain-slider', 'value'),
               State('pain-increase-checklist', 'value'),
               State('pain-decrease-checklist', 'value')])
def save_diary_to_sql(n_clicks, user, pain_level, getting_better, getting_worse):
    if n_clicks:
        unixtime = time.time()
        user_hash = user['user-hash']
        data = {
            "pain_level": pain_level,
            "getting_better": getting_better,
            "getting_worse": getting_worse
        }
        
        if (data['pain_level'] is None) or (data['pain_level'] < 0):  # pain must be filled in
            return html.H5(
                'Please fill in all data fields to continue :)', 
                style={'text-align': 'center', 'color': 'red'}
            )

        payload = json.dumps(data)
        sql_statement = f"""
           INSERT INTO pain_levels (user_hash, pain, unixtime) 
           VALUES ('{user_hash}', '{payload}', {unixtime})
           """
        sql.insert(sql_statement)
        return html.H5(
            'Got it - thanks so much!', 
            style={'text-align': 'center', 'color': 'green'}
        )


