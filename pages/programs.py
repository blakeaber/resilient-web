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
				dbc.Button("Manage Pain", href=f'exercises?pg={input_data["id"]}', color="primary"),
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

card_content_1 = create_card_from_data(data.PROGRAMS['general'])
card_content_2 = create_card_from_data(data.PROGRAMS['back'])

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
