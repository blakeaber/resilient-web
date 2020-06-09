from app import dbc, dcc, html


the_problem = dbc.Container([
	dbc.Row([
		dbc.Col(
            html.Img(
                src="./assets/BrokenSystem.png", 
                alt="Generic placeholder image"
            ), 
            width=6
        ),
		dbc.Col([
			dbc.CardBody(
				[
					html.H2("It's Expensive", className="card-title"),
					html.P("Employers lack transparency into actual costs", className="card-text"),
				]
			),
			dbc.CardBody(
				[
					html.H2("It's Inefficient", className="card-title"),
					html.P("Time to resolution is undervalued", className="card-text"),
				]
			),
			dbc.CardBody(
				[
					html.H2("It's Inconvenient", className="card-title"),
					html.P("Consumers are lost in the system", className="card-text"),
				]
			),
			dbc.CardBody(
				[
					html.H2("It's Complicated", className="card-title"),
					html.P("It is hard to relieve pain quickly at home", className="card-text"),
				]
			)
		], width=6)
	]),
	]
)


the_solution = dbc.Container([
	dbc.Row([
		dbc.Col([
		    dbc.CardBody([
				html.Img(src="./assets/SaveTime.png", alt="Generic placeholder image"),
				html.Hr(className='featurete-divider'),
				html.H2('Save Time'),
				html.P("By quickly treating physical pain in 5 days or less without visits or referrals."),
# 				html.P(
# 					dbc.Button('View details >>', href='#')
# 				)
		])], width=4),
		dbc.Col([
		    dbc.CardBody([
				html.Img(src="./assets/FeelBetter.png", alt="Generic placeholder image"),
				html.Hr(className='featurete-divider'),
				html.H2('Feel Better'),
				html.P("By conveniently addressing physical pain at home using only a smartphone."),
# 				html.P(
# 					dbc.Button('View details >>', href='#')
# 				)
		])], width=4),
		dbc.Col([
		    dbc.CardBody([
				html.Img(src="./assets/GetHelp.png", alt="Generic placeholder image"),
				html.Hr(className='featurete-divider'),
				html.H2('Get Help'),
				html.P("By efficiently generating high-quality diagnostic data for providers."),
# 				html.P(
# 					dbc.Button('View details >>', href='#')
# 				)
		])], width=4)
	]),
	]
)

call_to_action = jumbotron = dbc.Jumbotron(
    [
        html.H1("Address body pain anywhere, instantly"),
        html.P(
            "Our system is a digital therapeutic for musculoskeletal pain that "
            "provides AI-assisted, real-time feeback",
            className="lead"
        ),
        html.P(dbc.Button("Try It Out", href='/profile', color="primary", size='lg'), className="lead"),
    ]
)

final_chance = dbc.Button("Get Started", href='/profile', color="primary", size='lg', block=True)

featurettes = dbc.Container([
	dbc.Row([
		dbc.Col([
			html.H2('Triage For Overtreatment', className='featurette-heading'),
			html.Span("Many cases of musculoskeletal pain do not warrant a visit to a healthcare provider. ", className='text-muted'),
			html.Hr(className='featurete-divider'),
			html.P("The average incidence of musculoskeletal pain costs the healthcare system thousands of dollars and hours of somebody's time."),
			html.P("This platform will help you differentiate pain from actual injury to better identify when it's appropriate to seek the care of a medical provider."),
		], width=7, align='center'),
		dbc.Col([
			html.Img(className='featurette-image rounded-circle img-fluid mx-auto', src="https://miro.medium.com/max/640/1*tHn6JJJLeEcGM64uoi3XTA.png", alt="Generic placeholder image"),
		], width=5, align='center')
	], className='featurette'),
	dbc.Row([
		dbc.Col([
			html.Img(className='featurette-image rounded-circle img-fluid mx-auto', src="https://rehabconceptspt.com/wp-content/uploads/rehab-concepts-physical-therapy-therapy-sessions-isometric-illustration-1092x780.png", alt="Generic placeholder image"),
		], width=5, align='center'),
		dbc.Col([
			html.H2('The Movement Alphabet', className='featurette-heading'),
			html.Span("Gain the ability to access and control basic, foundational body positions", className='text-muted'),
			html.Hr(className='featurete-divider'),
			html.P("Pain does not always have a singular cause or source of 'damage'. In fact, many painful conditions result not because a body part or joint needs to be 'fixed' but because people lose the ability to access and control basic, foundational positions with their bodies."),
			html.P("We call these positions the movement alphabet."),
			html.P("This platform is designed to help you restore your movement alphabet and reserve in person musculoskeletal pain management for cases in which it is truly warranted.")
		], width=7, align='center')
	], className='featurette'),
	dbc.Row([
		dbc.Col([
			html.H2('Treat Yourself', className='featurette-heading'),
			html.Span("Reduce pain and prioritize your time and money", className='text-muted'),
			html.Hr(className='featurete-divider'),
			html.P("We want you to be able to care for yourself, regain confidence in your body, and reduce dependency on a system that doesn't always prioritize your time and money."),
			html.P("Try the daily routine we create for you for 5 days."),
			html.P("If you don't make any progress then consider seeking traditional care or relief."),
		], width=7, align='center'),
		dbc.Col([
			html.Img(className='featurette-image rounded-circle img-fluid mx-auto', src="https://blog.dnagenotek.com/hubfs/ACTN3%20gene%20with%20Oragene.jpg", alt="Generic placeholder image"),
		], width=5, align='center')
	], className='featurette'),
	html.Hr(className='featurete-divider')
	]
)

layout = html.Div(
    [
        dbc.Jumbotron(html.H1('Healthcare Has Problems')),
        the_problem,
        dbc.Jumbotron(html.H1('We Want To Help You')),
        the_solution,
        call_to_action,
        featurettes,
        final_chance,
        html.Hr(className='featurete-divider'),
        dbc.Alert("Our exercises might create a stretch sensation in certain muscles or a sensation of muscular effort. That's ok!"),
        dbc.Alert("Discontinue any exercise that increases your pain beyond your  baseline or normal level.", color="warning")
    ],
    className="text-center"
)
