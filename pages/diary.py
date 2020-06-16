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
    'No Change',
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
        dbc.Label("What Is Your Current Body Pain Level?", html_for="pain-slider"),
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


success_alert = dbc.Toast(
    'Thanks for the info!',
    id="pain-success-alert",
    header="Got It",
    is_open=True,
    dismissable=True,
    duration=4000,
    icon="success",
    style={"position": "fixed", "top": 100, "right": 10, "width": 350, "z-index": "999"}
)


fail_alert = dbc.Toast(
    "Please fill in all data fields to continue :)",
    id="pain-failure-alert",
    header="There was a problem...",
    is_open=True,
    dismissable=True,
    duration=4000,
    icon="danger",
    style={"position": "fixed", "top": 100, "right": 10, "width": 350, "z-index": "999"}
)


@app.callback(Output('diary-submit-status', 'children'),
              [Input('diary-submit-button', 'n_clicks')],
              [State('user-id', 'data'),
               State('pain-slider', 'value'),
               State('pain-increase-checklist', 'value'),
               State('pain-decrease-checklist', 'value')])
def save_diary_to_sql(n_clicks, user, pain_level, getting_better, getting_worse):
    def all_items_exist(data):
        has_pain_level = data['pain_level'] is not None
        has_better = any(data['getting_better'])
        has_worse = any(data['getting_worse'])
        return has_pain_level and has_better and has_worse

    if n_clicks:
        unixtime = time.time()
        user_hash = user['user-hash']
        data = {
            "pain_level": pain_level,
            "getting_better": getting_better or [],
            "getting_worse": getting_worse or []
        }
        
        if not all_items_exist(data):  # all values must be filled in
            return fail_alert

        payload = json.dumps(data)
        sql_statement = f"""
           INSERT INTO pain_levels (user_hash, pain, unixtime) 
           VALUES ('{user_hash}', '{payload}', {unixtime})
           """
        sql.insert(sql_statement)
        return success_alert


