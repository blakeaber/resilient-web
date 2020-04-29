from app import app, dbc, dcc, html, Input, Output, State
from pages import data, utils

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


layout = dbc.Jumbotron(
    [
        callout,
        dbc.Container(id='exercise-cards')
    ],
    fluid=True,
    className="text-center"
)


@app.callback(Output('exercise-cards', 'children'),
              [Input('url', 'href')],
              [State('url', 'pathname')])
def display_instructions(href, pathname):
    if pathname.startswith('/exercises'):
        program = utils.parse_url_parameters(href, param='pg')
        if program:
            exercise_cards = [
                create_card_from_data(data.EXERCISES[i]) 
                for i in data.PROGRAMS[program]['exercises']
            ]
        else:
            exercise_cards = [
                create_card_from_data(data.EXERCISES[i]) 
                for i in data.EXERCISES.keys()
            ]
        rows = utils.split_list_into_chunks(exercise_cards, chunk_size=3)
        return [
            dbc.Row([
                dbc.Col(card, width=4) for card in row
            ]) for row in rows
        ]
