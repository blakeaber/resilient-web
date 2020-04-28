from app import dbc, dcc, html

exercises = [
    {
        'name': 'Inch Worm',
        'description': 'Key pillar of the Movement Alphabet',
        'image-link': 'https://img.icons8.com/carbon-copy/2x/exercise.png',
        'target-areas': [ 'back', 'legs']
    },
    {
        'name': 'Couch Stretch',
        'description': 'Key pillar of the Movement Alphabet',
        'image-link': 'https://img.icons8.com/carbon-copy/2x/exercise.png',
        'target-areas': [ 'back', 'legs']
    }
]


jumbotron = dbc.Jumbotron(
    [
        dbc.Container(
            [
                html.H1("Movement Alphabet", className="jumbotron-cards"),
                html.P(
                    "We will introduce you to foundational movements "
                    "that will alleviate pain.",
                    className="lead",
                ),
                html.P(
                    "You will need to repeat the movements 3X daily.",
                    className="lead",
                ),
                html.P(
                    "If you continue to experience pain after 5 days, "
                    "seek out a clinician.",
                    className="lead",
                ),
            ],
            fluid=True,
        )
    ],
    fluid=True,
)

card_content_1 = dbc.Card([
    dbc.CardImg(src=exercises[0]['image-link'], top=True),
    dbc.CardBody(
        [
            html.H5(exercises[0]['name'], className="card-title"),
            html.P(
                exercises[0]['description'],
                className="card-text",
            ),
            dbc.Button("Get Started", color="primary"),
            html.Hr(),
            dbc.CardFooter([
	            html.P('Targets pain here:'),
                html.Span([
                    dbc.Badge(tag, pill=True, color="light", className="mr-1")
                    for tag in exercises[0]['target-areas']
                ])
            ])
        ]
    ),
], color="light", inverse=False)

card_content_2 = dbc.Card([
    dbc.CardImg(src=exercises[1]['image-link'], top=True),
    dbc.CardBody(
        [
            html.H5(exercises[1]['name'], className="card-title"),
            html.P(
                exercises[1]['description'],
                className="card-text",
            ),
            dbc.Button("Get Started", color="primary"),
            html.Hr(),
            dbc.CardFooter([
	            html.P('Targets pain here:'),
                html.Span([
                    dbc.Badge(tag, pill=True, color="light", className="mr-1")
                    for tag in exercises[1]['target-areas']
                ])
            ])
        ]
    ),
], color="light", inverse=False)

card_deck = dbc.CardDeck(
    [
        card_content_1,
        card_content_2
    ]
)

layout = dbc.Container([
    jumbotron,
    dbc.Container([
        dbc.Row(card_deck)
    ])
])

