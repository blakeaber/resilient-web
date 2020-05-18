from app import dbc, dcc, html, sql
from pages import utils


def create_card_from_data(input_data):
    return dbc.Card([
		dbc.CardImg(src=input_data['image_url'], top=True),
		dbc.CardBody(
			[
				html.H5(input_data['program'], className="card-title"),
				html.P(
					input_data['description'],
					className="card-text",
				),
				dbc.Button(
				    "Manage Pain", 
				    href=f'movement?pg={input_data["program_id"]}', 
				    color="primary"
				)
			]
		),
	], color="light", inverse=False)


callout = dbc.Container([
	html.H1("What Ails You?", className="jumbotron-cards"),
	html.P(
		"We all experience pain, stiffness or immobility at "
		"some point in our lives.",
		className="lead",
	),
	html.P(
		"Take control of pain management and address it at your convenience.",
		className="lead",
	)
], fluid=True)


program_cards = [
    create_card_from_data(program)
    for program in sql.select('select * from programs')
]


layout = dbc.Jumbotron(
    [
        callout,
        dbc.Container([
            dbc.Row([
                dbc.Col(card, width=4) for card in row
            ]) for row in utils.split_list_into_chunks(program_cards, chunk_size=3)
        ])
    ],
    fluid=True,
    className="text-center"
)
