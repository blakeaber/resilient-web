from app import dbc, dcc, html
from pages import data

def create_card_from_data(input_data):
    return dbc.Card([
		dbc.CardImg(src=input_data['image-link'], top=True),
		dbc.CardBody(
			[
				html.H5(input_data['name'], className="card-title"),
				html.P(
					input_data['description'],
					className="card-text",
				),
				dbc.Button("Get Moving", href=f'movement?ex={input_data["id"]}', color="primary"),
				html.Hr(),
				dbc.CardFooter([
					html.P('Targets pain here:'),
					html.Span([
						dbc.Badge(tag, pill=True, color="light", className="mr-1")
						for tag in input_data['target-areas']
					])
				])
			]
		),
	], color="light", inverse=False)

callout = dbc.Container([
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
], fluid=True)

card_content_1 = create_card_from_data(data.EXERCISES['inch-worm'])
card_content_2 = create_card_from_data(data.EXERCISES['couch-stretch'])

layout = dbc.Jumbotron(
    [
        callout,
        dbc.Container(dbc.Row([
            dbc.Col(card_content_1, width=4),
            dbc.Col(card_content_2, width=4),
            dbc.Col("", width=4),
        ])
        )
    ],
    fluid=True,
    className="text-center"
)
