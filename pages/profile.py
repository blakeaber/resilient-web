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
                {'label': 'N/A', 'value': '-'}
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
                5: 'Exercise Daily',
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
    dbc.Container([
		dbc.Row([
			dbc.Col([
				demographics
			], width=9), 
			dbc.Col(user_confirmation, width=3)
		], justify="center"),
		dbc.Row([
			dbc.Col(experience, width=12)
		], justify="center")
	]),
    dbc.Row([
        dbc.Col([
            html.Div(id='profile-submit-status'),
            dbc.Button("Submit", id='profile-submit-button', color="primary", block=True)
            ], 
            width=12
        )
    ], justify="center")
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
def display_selected_profile_data(sex, height, weight, activity, age):
    display_height = height
    if height:
	    height_remainder = height % 12
	    height_in_feet = int((height - height_remainder) / 12)
	    display_height = '{feet}ft {inches}in'.format(feet=height_in_feet, inches=height_remainder)

    return sex, display_height, weight, activity, age


@app.callback([Output('sex-radio', 'value'),
               Output('height-slider', 'value'),
               Output('weight-slider', 'value'),
               Output('activity-slider', 'value'),
               Output('age-slider', 'value'),
               Output('personal-experience-text', 'value'),
               Output('previous-pt-radio', 'value')],
              [Input('url', 'pathname')],
              [State('user-id', 'data')])
def store_selected_profile_data(pathname, user):
    if user.get('user-hash'):
        user_hash = user['user-hash']
        data = sql.select(f"""
            SELECT profile FROM profiles 
            WHERE user_hash = '{user_hash}'
            AND unixtime = (
                SELECT max(unixtime) 
                FROM profiles WHERE user_hash = '{user_hash}');
        """)

        if data:
            data = data[0][0]  # terrible!!!
            return (
                data['sex'], data['height'], data['weight'], 
                data['activity'], data['age'], data['experience'], 
                data['previous_pt']
            )

    return [None, 54, 50, None, None, None, None]


@app.callback(Output('profile-submit-status', 'children'),
              [Input('profile-submit-button', 'n_clicks')],
              [State('sex-radio', 'value'),
               State('height-slider', 'value'),
               State('weight-slider', 'value'),
               State('activity-slider', 'value'),
               State('age-slider', 'value'),
               State('personal-experience-text', 'value'),
               State('previous-pt-radio', 'value'),
               State('user-id', 'data')])
def save_profile_to_sql(n_clicks, sex, height, weight, activity, age, experience, pt, user):
    def all_items_exist(data):
        return all(data.values())

    data = {
        "sex": sex,
        "height": height,
        "weight": weight,
        "activity": activity,
        "age": age,
        "experience": experience,
        "previous_pt": pt
    }

    if n_clicks and user and all_items_exist(data):  # all values must be filled in
        unixtime = time.time()
        user_hash = user['user-hash']
        data['experience'] = data['experience'].replace("'", "''")            

        payload = json.dumps(data)
        sql_statement = f"""
           INSERT INTO profiles (user_hash, profile, unixtime) 
           VALUES ('{user_hash}', '{payload}', {unixtime})
           """
        sql.insert(sql_statement)
        return success_alert
    elif n_clicks and user:
        return fail_alert
    else:
        pass

