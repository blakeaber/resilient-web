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
from pages import howitworks, profile, diary, exercise, utils


INPUT_STEPS = [
    'Welcome',
    'Intro',
    'Profile',
    'Pain Level',
    'Exercises'
]


def create_process_steps_from_list(input_steps):
    total_steps = len(input_steps)
    if (total_steps > 12) or (total_steps < 1):
        return ValueError('Number of steps must be 1 <= steps <= 12!')

    step_width = 12 / total_steps
    return [
        dbc.Tab(
            id=f'onboard-tab-{step_idx+1}',
            tab_id=f'onboard-{step_idx+1}',
            label=step_text,
            label_style={
                'border': 'none',
                'border-color': 'none',
                'margin': '0 auto'
            },
            tab_style={'margin': '0 auto'}
        ) for step_idx, step_text in enumerate(input_steps)
    ]


welcome = dbc.Jumbotron(
    [
        html.H1("Welcome to Resilient AI", className="display-4"),
        html.P(
            "We're excited for your contribution to our platform, and "
            "we're here to help you!", className="lead"),
        html.Hr(className="my-2"),
        html.H3('What To Expect'),
        html.P(
            'We\'ll ask you to read about the platform and answer some '
            'preliminary questions about yourself. Once you do, we\'ll '
            'ask you to perform 3 exercises for 5 days in a row. '
            'Our expectation is that you\'ll help us succeed by '
            'committing to 15-30mins of exercise, daily.'),
        html.P(
            'For each exercise, we will provide a detailed video explaining what to do. '
            'The exercises should be approachable and should elicit a stretching sensation. '
            'Our hope is that the videos are very clear. If they\'re not, '
            'please tell us!'),
        html.P(
            'The goal of this engagement is to gather data for the `AI engine` '
            'that enables real-time feedback. We will do this by capturing videos of you '
            'exercising. We ask that you use either a laptop or tablet with a webcam. '),
        dbc.Button("Ready to go?", href='/onboard?next=2', color="success", size='lg', block=True),
        html.A(dbc.Button(
            "Confused? Contact Blake", 
            href='mailto: blake.aber@gmail.com', 
            color="secondary", size='md', block=True))
    ]
)


exercise_prep = dbc.Jumbotron(
    [
        html.H1("Great, all set!", className="display-4"),
        html.P(
            "We've got a simple program for you that focuses on "
            "foundational movements", className="lead"),
        html.Img(src="./assets/Wellness.jpg", style={'width': '100%'}),
        html.Hr(className="my-2"),
        html.H3('What You Need'),
        html.P(
            'Please wear athletic clothing and try to find ample floor space for stretching.'),
        html.P(
            'You\'ll need a couch or a chair to support your leg for one of the exercises.'),
        html.P(
            'Remember, you\'re just doing some stretching with friends and family, '
            'and maybe you\'ll have fun!'),
        dbc.Button("Ready to go?", href='/exercise', color="success", size='lg', block=True)
    ]
)


progress_alert = dbc.Toast(
    "Please continue to the next step :)",
    id="progress-alert",
    header="Thanks for the info!",
    is_open=True,
    dismissable=True,
    duration=4000,
    icon="success",
    style={"position": "fixed", "top": 10, "right": 10, "width": 350, "z-index": "999"}
),


layout = dbc.Container([
    html.Br(),
    dcc.Store(id='profile-complete', storage_type='memory'),
    dcc.Store(id='diary-complete', storage_type='memory'),
    html.Div(id='profile-upload-alert'),
    html.Div(id='diary-upload-alert'),
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
    html.Div(id='onboarding-submit-status'),
    html.Div(id='onboarding-content')
])


@app.callback([Output('onboarding-content', 'children'),
               Output('progress-steps', 'value')],
              [Input('onboarding-steps', 'active_tab')])
def display_page(active_tab):
    if not active_tab or (active_tab == 'onboard-1'):
        return welcome, 10
    elif active_tab == 'onboard-2':
        return howitworks.layout, 27
    elif active_tab == 'onboard-3':
        return profile.onboard_layout, 43
    elif active_tab == 'onboard-4':
        return diary.onboard_layout, 62
    elif active_tab == 'onboard-5':
        return exercise_prep, 80
    else:
        return html.P('This indicates an error has occured :(')


@app.callback([Output('profile-complete', 'data'),
               Output('profile-upload-alert', 'children')],
              [Input('url', 'pathname'),
               Input('sex-radio', 'value'),
               Input('height-slider', 'value'),
               Input('weight-slider', 'value'),
               Input('activity-slider', 'value'),
               Input('age-slider', 'value'),
               Input('personal-experience-text', 'value'),
               Input('previous-pt-radio', 'value')],
              [State('user-id', 'data')])
def save_profile_to_sql(pathname, sex, height, weight, activity, age, experience, pt, user):
    is_profile_complete = False
    alert_to_post = None

    data = {
        "sex": sex,
        "height": height,
        "weight": weight,
        "activity": activity,
        "age": age,
        "experience": experience,
        "previous_pt": pt
    }

    if user and all(data.values()):  # all values must be filled in
        unixtime = time.time()
        user_hash = user['user-hash']
        data['experience'] = data['experience'].replace("'", "''")            

        payload = json.dumps(data)
        sql_statement = f"""
           INSERT INTO profiles (user_hash, profile, unixtime) 
           VALUES ('{user_hash}', '{payload}', {unixtime})
           """
        sql.insert(sql_statement)

        is_profile_complete = True
        alert_to_post = progress_alert
    
    return is_profile_complete, alert_to_post


@app.callback([Output('diary-complete', 'data'),
               Output('diary-upload-alert', 'children')],
              [Input('url', 'pathname'),
               Input('pain-slider', 'value'),
               Input('pain-increase-checklist', 'value'),
               Input('pain-decrease-checklist', 'value')],
              [State('user-id', 'data'),
               State('profile-complete', 'data')])
def save_diary_to_sql(pathname, pain_level, getting_better, getting_worse, user, profile_complete):
    is_diary_complete = False
    alert_to_post = None

    def all_items_exist(data):
        has_pain_level = data['pain_level'] is not None
        has_better = (data['getting_better'] is not None) and any(data['getting_better'])
        has_worse = (data['getting_worse'] is not None) and any(data['getting_worse'])
        return has_pain_level and has_better and has_worse

    if not profile_complete:
        return is_diary_complete, alert_to_post
    else:
        data = {
            "pain_level": pain_level,
            "getting_better": getting_better or [],
            "getting_worse": getting_worse or []
        }

        if all_items_exist(data):  # all values must be filled in
            unixtime = time.time()
            user_hash = user['user-hash']

            payload = json.dumps(data)
            sql_statement = f"""
               INSERT INTO pain_levels (user_hash, pain, unixtime) 
               VALUES ('{user_hash}', '{payload}', {unixtime})
               """
            sql.insert(sql_statement)

            is_diary_complete = True
            alert_to_post = progress_alert
    
    return is_diary_complete, alert_to_post


@app.callback([Output('onboard-tab-4', 'disabled'),
               Output('onboard-tab-5', 'disabled')],
              [Input('url', 'pathname'),
               Input('profile-complete', 'data'),
               Input('diary-complete', 'data')])
def save_diary_to_sql(pathname, profile_complete, diary_complete):
    return not profile_complete, not diary_complete


@app.callback(Output('onboarding-steps', 'active_tab'),
              [Input('url', 'href')],
              [State('url', 'pathname')])
def skip_to_tab_from_intro(href, pathname):
    if pathname.startswith('/onboard'):
        next_tab = utils.parse_url_parameters(href, param='next')
        if next_tab:
	        return f'onboard-{next_tab}'

