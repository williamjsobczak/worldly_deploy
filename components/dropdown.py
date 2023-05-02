import dash
from dash import html, dcc
import ids
import data

def render(app: dash.Dash) -> html.Div:
    all_queries = ["Query 1", "Query 2", "Query 3"]
    return html.Div(
        children=[
            html.H6("Query"),
            dcc.Dropdown(
                id=ids.QUERY_DROPDOWN,
                options=[{"label": query, "value": query} for query in all_queries],
                value=all_queries
            )
        ])
