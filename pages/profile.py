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


previous_pt = dbc.FormGroup(
    [
        dbc.Label("Previous Physical Therapy", html_for="previous-pt-radio"),
        dbc.RadioItems(
            id="previous-pt-radio",
            options=[
                {'label': 'Yes', 'value': 'Y'},
                {'label': 'No', 'value': 'N'}
            ],
            inline=True
        )
    ]
)

personal_history = dbc.FormGroup(
    [
        dbc.Label("Personal Experience", html_for="personal-experience-text"),
        dbc.Textarea(
            id='personal-experience-text',
            placeholder="""
             - Tell me about the last time you had an injury that required some time to recover
             - What did you do to recover from that injury?
             - What tools and/or resources did you use to help you recover?
            """,
            bs_size="lg",
            style={'height': 200}
        )
    ]
)

sex = dbc.FormGroup(
    [
        dbc.Label("Sex", html_for="sex-radio"),
        dbc.RadioItems(
            id="sex-radio",
            options=[
                {'label': 'Male', 'value': 'M'},
                {'label': 'Female', 'value': 'F'},
                {'label': 'Other', 'value': '-'}
            ],
            inline=True
        )
    ]
)

height = dbc.FormGroup(
    [
        dbc.Label("Height (in)", html_for="height-slider"),
        dcc.Slider(
            id="height-slider", 
            min=54, 
            max=80, 
            step=1, 
            marks={
                60: '5ft',
                66: '5ft 6in',
                72: '6ft',
            },
            updatemode='drag'
        ),
    ]
)

weight = dbc.FormGroup(
    [
        dbc.Label("Weight (lbs)", html_for="weight-slider"),
        dcc.Slider(
            id="weight-slider", 
            min=50, 
            max=250, 
            step=1,
            marks={
                100: '100',
                150: '150',
                200: '200'
            },
            updatemode='drag'
        ),
    ]
)

activity_level = dbc.FormGroup(
    [
        dbc.Label("Activity Level", html_for="activity-slider"),
        dcc.Slider(
            id="activity-slider", 
            min=0, 
            max=10, 
            step=1, 
            marks={
                0: 'Sedentary',
                5: 'Daily Exercise',
                10: 'Olympic Athlete'
            },
            updatemode='drag'
        ),
    ]
)

age_group = dbc.FormGroup(
    [
        dbc.Label("Age", html_for="age-slider"),
        dcc.Slider(
            id="age-slider", 
            min=0, 
            max=90, 
            step=1, 
            marks={
                20: '20',
                30: '30',
                40: '40',
                50: '50',
                60: '60',
                70: '70'
            },
            updatemode='drag'
        ),
    ]
)


demographics = dbc.Card([
    dbc.CardHeader("Demographics"),
    dbc.CardBody(
        dbc.Form([
            sex,
            height,
            weight,
            age_group,
            activity_level
        ])
    )
], color="light", outline=True)


experience = dbc.Card([
    dbc.CardHeader("Baseline"),
    dbc.CardBody(
        dbc.Form([
            personal_history,
            previous_pt
        ])
    )
], color="light", outline=True)


user_confirmation = dbc.Card([
    dbc.CardHeader("Selected"),
    dbc.CardBody([
        html.H5('Sex'),
        html.Div(id='sex-display')
    ]),
    dbc.CardBody([
        html.H5('Height'),
        html.Div(id='height-display')
    ]),
    dbc.CardBody([
        html.H5('Weight'),
        html.Div(id='weight-display')
    ]),
    dbc.CardBody([
        html.H5('Age'),
        html.Div(id='age-display')
    ]),
    dbc.CardBody([
        html.H5('Activity'),
        html.Div(id='activity-display')
    ])
], color="light", outline=True)


layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            demographics
        ], width=9), 
        dbc.Col(user_confirmation, width=3)
    ], justify="center"),
    dbc.Row([
        dbc.Col([
            experience,
#             html.A(
                dbc.Button("Submit", id='profile-submit-button', color="primary", block=True),
#                 href='/diary'
#             ),
            html.Div(id='profile-success-message')
            ], 
            width=12
        )
        
    ], justify="center")
])


@app.callback([Output('sex-display', 'children'),
               Output('height-display', 'children'),
               Output('weight-display', 'children'),
               Output('activity-display', 'children'),
               Output('age-display', 'children')],
              [Input('sex-radio', 'value'),
               Input('height-slider', 'value'),
               Input('weight-slider', 'value'),
               Input('activity-slider', 'value'),
               Input('age-slider', 'value')])
def disable_tabs_while_recording(sex, height, weight, activity, age):
    return sex, height, weight, activity, age


@app.callback(Output('profile-success-message', 'children'),
              [Input('profile-submit-button', 'n_clicks')],
              [State('user-id', 'data'),
               State('sex-radio', 'value'),
               State('height-slider', 'value'),
               State('weight-slider', 'value'),
               State('activity-slider', 'value'),
               State('age-slider', 'value'),
               State('personal-experience-text', 'value'),
               State('previous-pt-radio', 'value')
              ])
def save_profile_to_sql(n_clicks, user, sex, height, weight, activity, age, experience, pt):
    if n_clicks:
        user_hash = user['user-hash']
        payload = json.dumps({
            "sex": sex,
            "height": height,
            "weight": weight,
            "activity": activity,
            "age": age,
            "experience": experience,
            "previous_pt": pt
        })
        sql_statement = "INSERT INTO profiles (user_hash, profile) VALUES ('{user_hash}', '{payload}')".format(
            user_hash=user_hash, 
            payload=payload
        )
        sql.insert(sql_statement)
        sql.insert("INSERT INTO profiles (user_hash) VALUES ('donny2')")
        return html.P(sql_statement)
