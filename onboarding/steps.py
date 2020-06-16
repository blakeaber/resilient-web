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


welcome = html.P('Welcome!!!')


layout = dbc.Container([
    html.Br(),
    dcc.Store(id='profile-complete', storage_type='memory'),
    dcc.Store(id='diary-complete', storage_type='memory'),
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
        return profile.onboard_layout, 32
    elif active_tab == 'onboard-3':
        return diary.onboard_layout, 55
    elif active_tab == 'onboard-4':
        return welcome, 78
#         return exercise.layout
    else:
        return html.P('This indicates an error has occured :(')


@app.callback(Output('profile-complete', 'data'),
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
    
    return is_profile_complete


@app.callback(Output('diary-complete', 'data'),
              [Input('url', 'pathname'),
               Input('pain-slider', 'value'),
               Input('pain-increase-checklist', 'value'),
               Input('pain-decrease-checklist', 'value')],
              [State('user-id', 'data'),
               State('profile-complete', 'data')])
def save_diary_to_sql(pathname, pain_level, getting_better, getting_worse, user, profile_complete):
    is_diary_complete = False

    def all_items_exist(data):
        has_pain_level = data['pain_level'] is not None
        has_better = (data['getting_better'] is not None) and any(data['getting_better'])
        has_worse = (data['getting_worse'] is not None) and any(data['getting_worse'])
        return has_pain_level and has_better and has_worse

    if not profile_complete:
        return is_diary_complete
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
    
    return is_diary_complete


@app.callback([Output('onboard-tab-3', 'disabled'),
               Output('onboard-tab-4', 'disabled')],
              [Input('url', 'pathname'),
               Input('profile-complete', 'data'),
               Input('diary-complete', 'data')])
def save_diary_to_sql(pathname, profile_complete, diary_complete):
    return not profile_complete, not diary_complete


