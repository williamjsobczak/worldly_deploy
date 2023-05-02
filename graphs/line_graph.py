import dash
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy as np

import plotly.graph_objs as go

from dash import html, dcc
from dash import dash_table
from components.navbar import navbar
from components.footer import footer

import components.dropdown as dropdown
import ids
import functions
import data

# Set up blank line graph
blank_df = pd.DataFrame()
blank_fig = px.line(blank_df)

line_graph_section = dbc.Container([
        dbc.Row(
            dbc.Col(
                [
                    html.H1('Visualization of a Parameter over Time'),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.H4('Select the parameter to view over time, as well as which subset of countries to display.'),
                    dcc.Dropdown(
                        id=ids.LINE_GRAPH_DROPDOWN,
                        options=[{'label': i, 'value': i} for i in data.attribute_table_dict.keys()],
                        value=None,
                        multi=False,
                        className = 'dropdown-style',
                    ),
                    html.Br(),
                    html.Br(),
                    dcc.Dropdown(
                        id=ids.TOP_BOTTOM_DROPDOWN,
                        options=[{'label': i, 'value': i} for i in data.line_graph_top_bottom],
                        value=None,
                        multi=False,
                        className = 'dropdown-style',
                    ),
                    html.Br(),
                    html.Br(),
                    dcc.Dropdown(
                        id=ids.LINE_GRAPH_NUMBER_RESTRICTION_DROPDOWN,
                        options=[{'label': i, 'value': i} for i in data.line_graph_number_options],
                        value=None,
                        multi=False,
                        className = 'dropdown-style',
                    ),
                ],
                style={'margin-top': '50px', 'margin-bottom': '50px'},
                className='centered'
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            children=[
                                dcc.Graph(
                                    id=ids.LINE_GRAPH,
                                    figure=blank_fig,
                                ),
                            ],
                            id=ids.LINE_GRAPH_CONTAINER,
                        )
                    ]
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            children=[
                                dcc.Graph(
                                    id=ids.CONTINENT_LINE_GRAPH,
                                    figure=blank_fig,
                                ),
                            ],
                            id=ids.CONTINENT_LINE_GRAPH_CONTAINER,
                        )
                    ]
                )
            ]
        ),
    ],
    className = 'scatter-plot-container'
)


def render():
    return line_graph_section

def render_line_graph_country(parameter, sorting_option, restriction_number):

    table_with_the_parameter = data.attribute_table_dict[parameter]
    formatted_parameter = functions.format_attribute_name_for_sql(parameter).upper()
    top_or_bottom = ''

    if sorting_option == data.line_graph_top_bottom[0]:
        # TOP 10
        ordering = 'DESC'
        top_or_bottom = 'Top'
    elif sorting_option == data.line_graph_top_bottom[1]:
        # BOTTOM 10
        ordering = 'ASC'
        top_or_bottom = 'Bottom'
    else:
        # DEFAULT: TOP 10
        ordering = 'DESC'
        top_or_bottom = 'Top'

    query_string_country = f'SELECT entity, year, {formatted_parameter} FROM ' \
                    f'( SELECT continents.entity, continents.code, placeholder_table.year, placeholder_table.{formatted_parameter} , RANK() OVER(PARTITION BY year ORDER BY placeholder_table.{formatted_parameter} {ordering}) rank_num '\
                    f'FROM {table_with_the_parameter} placeholder_table, (SELECT entity, code, continent FROM Continents) continents '\
                    f'WHERE year >= 1900 AND placeholder_table.{formatted_parameter} IS NOT NULL AND placeholder_table.code NOT LIKE \'%OWID%\' AND placeholder_table.code = continents.code ) WHERE rank_num<={restriction_number}'    

    df = functions.query_db(query_string_country)
    
    # print(query_string_country)
    # print(df.head(10))


    fig_country = px.line(df, x="YEAR", y=formatted_parameter, color="ENTITY", line_group="ENTITY", hover_name="ENTITY")
    fig_country = fig_country.update_layout(width=1250, height=800)
    fig_country.update_xaxes(title_text='Year')
    fig_country.update_yaxes(title_text=parameter)
    fig_country.update_layout(title=f'\'{parameter}\' vs Time for the {top_or_bottom} {restriction_number} Countries')

    line_graph_figure = html.Div(children=[
            dcc.Graph(id='data-visualization', figure=fig_country)
    ], className="centered")


    return line_graph_figure

def render_line_graph_continent(parameter):
    table_with_the_parameter = data.attribute_table_dict[parameter]
    formatted_parameter = functions.format_attribute_name_for_sql(parameter).upper()

    query_string_continent = f'SELECT continents.continent, year, AVG(  {formatted_parameter}) '\
                                f'FROM   {table_with_the_parameter} table_placeholder, (SELECT entity, code, continent FROM Continents) continents WHERE   {formatted_parameter} IS NOT NULL AND continents.code =  table_placeholder.code AND table_placeholder.year >=1900 '\
                                f'GROUP BY continents.continent, year'
    
    df = functions.query_db(query_string_continent)
    df = df.sort_values(by=['YEAR'])

    # print(query_string_continent)
    # print(df.head(100))

    fig_continent = px.line(df, x="YEAR", y=f'AVG({formatted_parameter})', color="CONTINENT", line_group="CONTINENT", hover_name="CONTINENT")
    fig_continent = fig_continent.update_layout(width=1250, height=800)
    fig_continent.update_xaxes(title_text='Year')
    fig_continent.update_yaxes(title_text=parameter)
    fig_continent.update_layout(title=f'\'{parameter}\' vs Time for each Continent')

    line_graph_figure = html.Div(children=[
            dcc.Graph(id='data-visualization', figure=fig_continent)
    ], className="centered")

    return line_graph_figure

