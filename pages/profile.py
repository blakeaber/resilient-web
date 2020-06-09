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
        dbc.Checklist(
            id="body-pain-checklist",
            options=[
                {"label": i, "value": idx} for idx, i in enumerate(pain_areas)
            ],
#             labelStyle={'display': 'inline-block', 'margin': '10px'},
#             inputStyle={'margin': '5px'},
            switch=True,
            inline=True
        )
    ]
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
				{'label': 'Other', 'value': 'O'}
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
            min=50, 
            max=250, 
            step=10,
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
            min=20, 
            max=70, 
            step=10, 
            marks={
                20: '18 – 24',
                30: '25 – 34',
                40: '35 – 44',
                50: '45 – 54',
                60: '55 – 64',
                70: '65+'
            }
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
			body_pain_checklist,
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
            dbc.Button("Submit", id='profile-submit-button', color="primary", block=True)
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

