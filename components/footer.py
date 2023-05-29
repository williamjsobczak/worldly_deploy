import dash
import dash_bootstrap_components as dbc
from dash import html


def footer():

    ftr = html.Div(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div([
                                html.H5("world.ly", className="text-uppercase footer-title"),
                            ]),
                            className="centered"
                        ),
                    ],
                    style={"margin-bottom": "30px"},
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div([
                                html.H5("Quick Links", className="text-uppercase"),
                                dbc.NavLink("Home", href="/", className = "footer-link"),
                                dbc.NavLink("About", href="/about", className = "footer-link"),
                                dbc.NavLink("How to Use", href="/how_to", className = "footer-link"),
                                dbc.NavLink("Get Started", href="/app", className = "footer-link")                               
                            ]),
                            className="centered"
                        ),
                        dbc.Col(
                            html.Div([
                                html.Br(),
                                html.Br(),
                                html.P("🌎🌍🌏"),
                            ]),
                            className="centered",
                            md=2
                        ),
                        dbc.Col(
                            html.Div([
                                html.Br(),
                                html.Br(),
                                html.A(
                                    "GitHub Repository",
                                    href='https://github.com/WilliamSobczak/worldly_deploy.git',
                                    target="_blank",
                                    style={'font-size': '25px'}
                                )
                            ]),
                            className="centered"
                        ),
                    ],
                    className="justify-content-center"
                ),
            ],
            fluid=True,
        ),
        className="p-5 mt-5 bg-light",
        style={"margin-top": "30px"},
    )
    return ftr