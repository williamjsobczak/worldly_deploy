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

# -------------------------------------------- INITAL QUERY NEEDED TO SET UP SCATTER PLOT -------------------------------------------- #
query_string = 'SELECT education.code, education.entity, education.year, education.percentage_with_tertiary_education percentage_with_tertiary_education, income.gross_national_income_per_capita per_capita_income FROM ShareOfThePopulationWithCompletedTertiaryEducation education, GrossNationalIncomePerCapita income WHERE education.code = income.code AND education.year = income.year AND education.year = \'2010\' '
df = functions.query_db(query_string)
# x='PERCENTAGE_WITH_TERTIARY_EDUCATION'
# y='PER_CAPITA_INCOME'
# coefficients = np.polyfit(x, y, 1)
# line = coefficients[0] * x + coefficients[1]
scatter_fig = px.scatter(df, x='PERCENTAGE_WITH_TERTIARY_EDUCATION', y='PER_CAPITA_INCOME', hover_name='ENTITY', color='ENTITY')
scatter_fig.update_xaxes(title_text=(functions.reformat_data_label("PERCENTAGE_WITH_TERTIARY_EDUCATION")))
scatter_fig.update_yaxes(title_text=(functions.reformat_data_label("PER_CAPITA_INCOME")))
# scatter_fig.add_trace(px.line(x=x, y=line).data[0])
scatter_fig.update_layout(width=1300, height=1000)
# -------------------------------------------- INITAL QUERY NEEDED TO SET UP SCATTER PLOT -------------------------------------------- #


# -------------------------- MAIN SCATTER PLOT SECTION -------------------------- #

scatter_plot_section = dbc.Container(
    [
    # Add dropdown and buttons here
        dbc.Row(
            dbc.Col(
                [
                html.H1('Compare Two Parameters Over Time'),
                html.Br(),
                html.Br(),
                html.Br(),
                html.H4('Choose two metrics.'),
                dcc.Dropdown(
                    id=ids.SCATTER_PLOT_DROPDOWN_1,
                    options=[{'label': i, 'value': i} for i in data.attribute_table_dict.keys()],
                    value=None,
                    multi=False,
                    className = 'dropdown-style',
                ),
                html.Br(),
                html.Br(),
                dcc.Dropdown(
                    id=ids.SCATTER_PLOT_DROPDOWN_2,
                    options=[{'label': i, 'value': i} for i in data.attribute_table_dict.keys()],
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
                                    id=ids.STATIC_SCATTER_PLOT,
                                    figure=scatter_fig,
                                ),
                            ],
                            id=ids.STATIC_SCATTER_PLOT_CONTAINER,
                        )
                    ]
                )
            ]
        ),
    ],
    className = 'scatter-plot-container'
)

# -------------------------- MAIN SCATTER PLOT SECTION -------------------------- #



# RENDER THE MAIN SCATTER PLOT SECTION
def render():
    return scatter_plot_section


# QUERY NEEDED FOR CREATING SCATTER PLOT
def query_for_static_scatter_plot(parameter1, parameter2):

    table1 = data.attribute_table_dict[parameter1]
    table2 = data.attribute_table_dict[parameter2]

    parameter1 = functions.format_attribute_name_for_sql(parameter1)
    parameter2 = functions.format_attribute_name_for_sql(parameter2)

    # print(parameter1)
    # print(parameter2)
    # print(table1)
    # print(table2)

    query_string = f'SELECT continents.entity, table1.{parameter1} parameter1, table2.{parameter2} parameter2, table1.year ' \
    f'FROM {table1} table1, {table2} table2, (SELECT entity, code, continent FROM Continents) continents ' \
    f'WHERE table1.code = table2.code AND table1.year = table2.year AND continents.code = table1.code AND table1.code NOT LIKE \'%OWID%\' AND table1.{parameter1} IS NOT NULL AND table2.{parameter2} IS NOT NULL ' \
    f'ORDER BY table1.year ASC'

    print(query_string)

    df = functions.query_db(query_string)
    return df

