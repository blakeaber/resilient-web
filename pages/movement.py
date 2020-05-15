from app import (
    app, 
    dbc, 
    dcc, 
    html, 
    Input, 
    Output, 
    State,
    sql
    )
from pages import utils


typeform_iframe = html.Iframe(
    id='give-feedback', 
    src='https://ba881.typeform.com/to/hJ6vPg',
    width='100%',
    height=400
)


modal_feedback = dbc.Modal(
    [
        dbc.ModalHeader("Quick Survey", style={'float': 'left'}),
        dbc.ModalBody(typeform_iframe),
        dbc.ModalFooter(dbc.Button("Close", id="close-modal-feedback", style={'float': 'right'}))
    ],
    id="modal-feedback",
    size='xl',
    backdrop='static',
    centered=True
)


feedback_request = dbc.Button("Help Us Improve", id="open-modal-feedback", color='success')


modal_ai = dbc.Modal(
            [
                dbc.ModalHeader("Awesome pose estimation AI!"),
                dbc.ModalBody("HTML Video, on/off recording buttons, etc"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-modal-ai")
                ),
            ],
            id="video-modal-ai",
            size="xl"
        )


card_content_1 = dbc.CardHeader([
    dbc.Tabs(
        [
            dbc.Tab(label="Movement 1", tab_id="movement-1"),
            dbc.Tab(label="Movement 2", tab_id="movement-2"),
            dbc.Tab(label="Movement 3", tab_id="movement-3")
        ],
        id="movement-tabs",
        card=True
    )
])
card_1 = dbc.Card(card_content_1, color="light", outline=True)


card_content_2 = dbc.CardBody([
    feedback_request,
    modal_feedback
])
card_2 = dbc.Card(card_content_2, color="light", outline=True)


card_content_3 = dbc.CardBody([
    dbc.Button([
        "digital  ", 
        html.Img(width=35, src='https://static.thenounproject.com/png/2486348-200.png'),
        "  feedback", 
    ], 
    id="open-modal-ai",
    color='success')
])
card_3 = dbc.Card(card_content_3, color="light", outline=True)



card_content_4 = dbc.CardBody([
    html.Iframe(
        id='instruction-video',
        width=600,
        height=400
    )
])
card_4 = dbc.Card(card_content_4, color="light", outline=True)



card_content_5 = [
    dbc.CardHeader("Details"),
    dbc.CardBody([
        html.H5("Difficulty", className="card-title"),
        dbc.Button("Advanced", id='advanced-button', size='med')
    ]),
    dbc.CardBody([
        html.H5("Watch Out For", className="card-title"),
        dbc.ListGroup(
            id='watch-out-for',
            flush=True,
        )
    ])
]
card_5 = dbc.Card(card_content_5, color="light", outline=True)


# TODO: put BOTH the instructional video AND the video recording in a modal (to save space)!!!
cards = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col(card_1, width=12)
            ], justify="center"),
            dbc.Row([
                dbc.Col(card_4, width=12)
            ], justify="center"),
            dbc.Row([
                dbc.Col(card_2, width=6, align='center'),
                dbc.Col(card_3, width=6, align='center')
            ], justify="center"),
        ], width=7), 
        dbc.Col(card_5, width=5)
    ], justify="center")
])


layout = dbc.Container([
    cards,
    modal_ai
    ])


@app.callback(Output('advanced-button', 'active'),
              [Input('advanced-button', 'n_clicks')])
def make_active_flag(n_clicks):
    if n_clicks:
        return n_clicks % 2 == 1
    else:
        return False


@app.callback([Output('instruction-video', 'src'),
               Output('watch-out-for', 'children')],
              [Input('url', 'href'),
               Input('advanced-button', 'active'),
               Input('movement-tabs', 'active_tab')],
               [State('url', 'pathname')])
def display_program_movement(href, button_active, active_tab, pathname):
    if pathname.startswith('/movement'):
        program = utils.parse_url_parameters(href, param='pg')
        movement = active_tab.split('-')[1]
        difficulty = int(button_active)
        if program:
            program_content = sql.select(f"""
				select instruction 
				from instructions
				where instruction_id in 
				(select instruction_id
				from program_content
				where program_id={program}
				and exercise_group={movement}
				and difficulty_level={difficulty})
                """)

            exercise_details = sql.select(f"""
				select video_url from exercises
				where exercise_id = 
				(select distinct exercise_id 
				from program_content
                where program_id={program} 
                and exercise_group={movement} 
                and difficulty_level={difficulty})
                """)
            exercise_details = next(exercise_details)
            
            watch_outs = [dbc.ListGroupItem(item) for item in program_content]
            
            return exercise_details['video_url'], watch_outs


@app.callback(
    Output("modal-feedback", "is_open"),
    [Input("open-modal-feedback", "n_clicks"), 
    Input("close-modal-feedback", "n_clicks")],
    [State("modal-feedback", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output("video-modal-ai", "is_open"),
    [Input("open-modal-ai", "n_clicks"), Input("close-modal-ai", "n_clicks")],
    [State("video-modal-ai", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
