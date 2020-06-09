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


body_pain_checklist = dbc.FormGroup(
    [
        dbc.Label("Body Pain", html_for="body-pain-checklist"),
        dcc.Checklist(
            id="body-pain-checklist",
            options=[
                {"label": i, "value": i.lower()} for i in pain_areas
            ],
            labelStyle={'display': 'inline-block', 'margin': '10px'},
            inputStyle={'margin': '5px'}
        )
    ]
)

previous_pt = dbc.FormGroup(
    [
        dbc.Label("Previous Physical Therapy", html_for="previous-pt-radio"),
        dcc.RadioItems(
            id="previous-pt-radio",
            options=[
				{'label': 'Yes', 'value': 'Y'},
				{'label': 'No', 'value': 'N'}
            ],
            labelStyle={'display': 'inline-block', 'margin': '10px'},
            inputStyle={'margin': '5px'}
        )
    ]
)

personal_history = dbc.FormGroup(
    [
        dbc.Label("Personal Experience", html_for="personal-experience-text"),
		dcc.Textarea(
		    id='personal-experience-text',
			placeholder="""
			 - Tell me about the last time you had an injury that required some time to recover
			 - What did you do to recover from that injury?
			 - What tools and/or resources did you use to help you recover?
			""",
			style={'width': '100%', 'height': 150}
		)
	]
)

sex = dbc.FormGroup(
    [
        dbc.Label("Sex", html_for="sex-radio"),
        dcc.RadioItems(
            id="sex-radio",
            options=[
				{'label': 'Male', 'value': 'M'},
				{'label': 'Female', 'value': 'F'},
				{'label': 'Other', 'value': 'O'}
            ],
            labelStyle={'display': 'inline-block', 'margin': '10px'},
            inputStyle={'margin': '5px'}
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
            value=66,
            marks={
                60: '5ft',
                66: '5ft, 6in',
                72: '6ft',
            }
        ),
    ]
)

weight = dbc.FormGroup(
    [
        dbc.Label("Weight (lbs)", html_for="weight-slider"),
        dcc.Slider(
            id="weight-slider", 
            min=0, 
            max=300, 
            step=10,
            value=150,
            marks={
                100: '100',
                150: '150',
                200: '200'
            }
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
            value=3,
            marks={
                0: 'Sedentary',
                5: 'Daily Exercise',
                10: 'Olympic Athlete'
            }
        ),
    ]
)

age_group = dbc.FormGroup(
    [
        dbc.Label("Age", html_for="age-slider"),
        dcc.Slider(
            id="age-slider", 
            min=1, 
            max=6, 
            step=1, 
            marks={
                1: '18 – 24',
                2: '25 – 34',
                3: '35 – 44',
                4: '45 – 54',
                5: '55 – 64',
                6: '65+'
            }
        ),
    ]
)


profile_data = dbc.Card([
    dbc.CardHeader("Profile"),
    dbc.CardBody(
		dbc.Form([
			personal_history,
			body_pain_checklist,
			previous_pt,
			sex,
			age_group,
			height,
			weight,
			activity_level
		])
    )
], color="light", outline=True)


user_confirmation = dbc.Card([
    dbc.CardHeader("Selected"),
    dbc.CardBody([
        'THIS IS A TEST'
    ])
], color="light", outline=True)


layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            profile_data
        ], width=10), 
        dbc.Col(user_confirmation, width=2)
    ], justify="center"),
    dbc.Row([
        dbc.Button("Submit", id='profile-submit-button', color="primary")
    ], justify="center")
])


