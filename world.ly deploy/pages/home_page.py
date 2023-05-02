import dash
import dash_bootstrap_components as dbc

from dash import html
from dash import dcc
from components.navbar import navbar
from components.footer import footer

from dash_iconify import DashIconify


nav = navbar()
ftr = footer()

body = dbc.Container(
    [
        # First Row, contains the title/blurb and the spinning earth gif
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("world.ly", className="home-page-title"),
                        html.Br(),
                        # home page blurb
                        html.P(
                            """\
                            Welcome!
                            This application gives you the power to discover complex insights into global demographic data.\n world.ly
                            give you an insider view of pertinent global trends with respect to our broad category of parameters. Explore and compare metrics from
                            a variety of sectors (e.g., health, environment, education, economy, etc.) with our suite of dynamic, interactive visualizations.""",
                        ),
                        # Div for get started button
                        html.Div(
                            children=[
                                dcc.Link(
                                    html.Button(
                                        "Get Started",
                                        id="get-started-button",
                                        className="btn btn-lg btn-primary get-started-button",
                                        type="button"
                                    ),
                                    href="/app"
                                )
                            ],
                            className="centered",
                        )
                        
                    ],
                    md=6,
                ),
                dbc.Col(
                    [
                    # The spinning earth gif lmao
                        html.Img(
                            src="assets\images\earth.gif",
                            width="80%",
                            height="auto",
                            className="spinning-globe-gif"
                        )
                    ],
                    className="centered",
                    md=6,
                ),
            ]
        ),
        # New Row, contains sectors of interest title
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3("Sectors of Interest"),
                        html.Hr(),
                        html.Br(),
                    ]
                ),

            ],
            className="centered",
            style={"margin-top": "100px"},
        ),
        dbc.Row(
            [
                # Add a bunch of these dbc.Col to add icons for each sector
                dbc.Col(
                    [
                        html.H3("Economy"),
                        # Search for icons here: https://icon-sets.iconify.design/
                        # Replace the name of the icon in the icon="" field
                        DashIconify(
                            icon="ph:piggy-bank-duotone",
                            width=50,
                            height=50,
                        )
                    ],
                ),
                dbc.Col(
                    [
                        html.H3("Health"),
                        DashIconify(
                            icon="material-symbols:health-metrics",
                            width=50,
                            height=50,
                        )
                    ],
                ),
                dbc.Col(
                    [
                        html.H3("Society"),
                        DashIconify(
                            icon="material-symbols:emoji-people-rounded",
                            width=50,
                            height=50,
                        )
                    ],
                ),
                dbc.Col(
                    [
                        html.H3("Energy"),
                        DashIconify(
                            icon="mdi:energy-circle",
                            width=50,
                            height=50,
                        )
                    ],
                ),
                dbc.Col(
                    [
                        html.H3("Education"),
                        DashIconify(
                            icon="ri:graduation-cap-fill",
                            width=50,
                            height=50,
                        )
                    ],
                ),
                dbc.Col(
                    [
                        html.H3("Environment"),
                        DashIconify(
                            icon="mdi:pine-tree-variant",
                            width=50,
                            height=50,
                        )
                    ],
                ),
            ],
            className="centered",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Human Geography made simple."),
                        html.Br(),
                        html.P(
                            """\
                                Use world.ly to visualize hundreds of thousands of demographic data points.
                                """,
                        ),
                        
                    ],
                    className="centered",
                )
            ],
            style={"margin-top": "100px", "margin-bottom": "50px"},
        ),
    ],
    # mt-4 adds margin to the top
    className="mt-4 body-flex-wrapper",
)


def home_page(app: dash.Dash):
    layout = html.Div([nav, body, ftr], className="make-footer-stick")
    return layout