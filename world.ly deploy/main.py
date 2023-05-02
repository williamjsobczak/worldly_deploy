import dash
import cx_Oracle
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px

from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output

from pages.home_page import home_page
from pages.about_page import about_page
from pages.how_to_page import how_to_page
from pages.app_page import app_page

import plotly.graph_objs as go

import ids
import graphs.scatter_plot as scatter_plot
import numpy as np
import data
import graphs.world_map as world_map
import graphs.line_graph as line_graph

from pages.about_page import query_for_all_tuples

# Themes? Try FLATLY, LUX, QUARTZ
# https://towardsdatascience.com/3-easy-ways-to-make-your-dash-application-look-better-3e4cfefaf772
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.config.suppress_callback_exceptions = True
app.title = 'world.ly'

# Main layout
app.layout = html.Div([
    dcc.Location(id=ids.CURRENT_URL, refresh=False),
    html.Div(id=ids.CURRENT_PAGE_CONTENT)
])

# -------------------------------------------------- CALLBACKS -------------------------------------------------- #

# FUNCTION TO ROUTE TO DIFFERENT PAGES
@app.callback(
    Output(ids.CURRENT_PAGE_CONTENT, 'children'),
    [Input(ids.CURRENT_URL, 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return home_page(app)
    elif pathname == '/about':
        return about_page(app)
    elif pathname == '/how_to':
        return how_to_page(app)
    elif pathname == '/app':
        return app_page(app)
    else:
        return home_page(app)


# UPDATE SCATTER PLOT BASED ON DROPDOWN SELECTION
@app.callback(
    Output(ids.STATIC_SCATTER_PLOT_CONTAINER, 'children'),
    [Input(ids.SCATTER_PLOT_DROPDOWN_1, 'value'),
        Input(ids.SCATTER_PLOT_DROPDOWN_2, 'value')])
def update_line_graph(metric_1, metric_2):
    if metric_1 is None or metric_2 is None:
        return html.Div([html.H3('Please select two metrics to create a scatter plot. Use the dropdowns above.')], style={'textAlign': 'center', 'margin-top': '50px', 'margin-bottom': '50px'})
    else:
        df = scatter_plot.query_for_static_scatter_plot(metric_1, metric_2)
        all_countries = df['ENTITY'].unique().tolist()
        all_years = df['YEAR'].unique().tolist()
        complete_data = pd.DataFrame([(country, year) for country in all_countries for year in all_years], columns=['ENTITY', 'YEAR'])
        df = pd.merge(complete_data, df, on=['ENTITY', 'YEAR'], how='left')
        df['PARAMETER1'].replace(np.nan, None, inplace=True)
        df['PARAMETER2'].replace(np.nan, None, inplace=True)

        print(df.head())

    # ------------------------------------- OLD SCATTER PLOT ------------------------------------- #
    #     fig = px.scatter(df, x='PARAMETER1', y='PARAMETER2', hover_name='ENTITY', color='ENTITY', animation_frame='YEAR', animation_group='ENTITY')
    #         # animated_plot = px.scatter(df_animation, x='PERCENTAGE_WITH_TERTIARY_EDUCATION', y='PER_CAPITA_INCOME',
    # #                             animation_frame='YEAR',
    # #                             animation_group='ENTITY',
    # #                             hover_name='ENTITY', color='ENTITY')
    # ------------------------------------- OLD SCATTER PLOT ------------------------------------- #

        # Create a color scale for the countries
        country_color_scale = px.colors.qualitative.Plotly

        # Create the initial scatter trace
        scatter = go.Scatter(
            x=df.loc[df['YEAR'] == df['YEAR'].min(), 'PARAMETER1'],
            y=df.loc[df['YEAR'] == df['YEAR'].min(), 'PARAMETER2'],
            mode='markers',
            marker=dict(
                size=6,
                color=[country_color_scale[all_countries.index(country) % len(country_color_scale)]
                    for country in df.loc[df['YEAR'] == df['YEAR'].min(), 'ENTITY']],
            ),
            text=df.loc[df['YEAR'] == df['YEAR'].min(), 'ENTITY']
        )

        # Create the base figure with the initial trace
        fig = go.Figure(data=[scatter])

        # Define the animation frames with added annotations
        frames = [go.Frame(data=[go.Scatter(
            x=df.loc[df['YEAR'] == year, 'PARAMETER1'],
            y=df.loc[df['YEAR'] == year, 'PARAMETER2'],
            mode='markers',
            marker=dict(
                size=6,
                color=[country_color_scale[all_countries.index(country) % len(country_color_scale)]
                    for country in df.loc[df['YEAR'] == year, 'ENTITY']],
            ),
            text=df.loc[df['YEAR'] == year, 'ENTITY']
        )],
            layout=dict(
                annotations=[
                    dict(
                        x=1,
                        y=1.1,
                        xref="paper",
                        yref="paper",
                        text=f"Year: {year}",
                        showarrow=False,
                        font=dict(size=16),
                    )
                ]
            )
        ) for year in df['YEAR'].unique()]

        # Add the frames to the figure
        fig.frames = frames

        # Define animation settings
        animation_settings = dict(frame=dict(duration=500, redraw=True), fromcurrent=True)

        # Update layout to include the animation settings and set the initial frame
        fig.update_layout(
            updatemenus=[dict(type='buttons', showactive=False, buttons=[
                dict(label='Play', method='animate', args=[None, animation_settings]),
                dict(label='Pause', method='animate', args=[[None], dict(frame=dict(duration=0, redraw=True), fromcurrent=True, mode='immediate')])
            ])],
            title=f'Analysis of \'{metric_1}\' VS \'{metric_2}\'',
            xaxis=dict(title='PARAMETER1', autorange=True),
            yaxis=dict(title='PARAMETER2', autorange=True),
            annotations=[
                dict(
                    x=1,
                    y=1.1,
                    xref="paper",
                    yref="paper",
                    text=f"Year: {df['YEAR'].min()}",
                    showarrow=False,
                    font=dict(size=16),
                )
            ],
        )

        # Set axis autorange to update with animation
        fig.update_xaxes(autorange=True)
        fig.update_yaxes(autorange=True)


        # Update the axis titles and figure size
        fig.update_xaxes(title_text=metric_1)
        fig.update_yaxes(title_text=metric_2)
        fig.update_layout(width=1250, height=800)

        # Return the figure
        return dcc.Graph(id=ids.STATIC_SCATTER_PLOT, figure=fig)

# UPDATE COMPLEX QUERY WORLD MAP BASED ON DROPDOWN SELECTION
@app.callback(
    Output(ids.COMPLEX_QUERY_CONTAINER, 'children'),
    [Input(ids.COMPLEX_QUERY_DROPDOWN, 'value')])
def update_world_map(selection):
    if selection is None:
        return html.Div([html.H3('Please select an option to create the data visualizations')], style={'textAlign': 'center', 'margin-top': '20px', 'margin-bottom': '50px'})
    elif selection == data.complex_queries[0]:
        return world_map.render_world_map_1()
    elif selection == data.complex_queries[1]:
        return world_map.render_world_map_2()
    elif selection == data.complex_queries[2]:
        return world_map.render_world_map_3()
    elif selection == data.complex_queries[3]:
        return world_map.render_world_map_4()
    elif selection == data.complex_queries[4]:
        return world_map.render_world_map_5()
    else:
        return html.Div([html.H3('No valid selection')], style={'textAlign': 'center', 'margin-top': '20px', 'margin-bottom': '50px'})

#BUTTON FOR TOTAL NUMBER OF TUPLES
@app.callback(
    Output(ids.TOTAL_NUMBER_TUPLES_CONTAINER, 'children'),
    [Input(ids.TOTAL_TUPLES_BUTTON, 'n_clicks')])
def display_total_tuples(n_clicks):
    if n_clicks is not None:
       return html.Div([html.H3(f"Total number of data points (tuples) in our dataset: {query_for_all_tuples()}")], style={'textAlign': 'center', 'margin-top': '20px', 'margin-bottom': '50px'})


# DROPDOWNS FOR LINE PLOT SECTION
@app.callback(
    Output(ids.LINE_GRAPH_CONTAINER, 'children'),
    [Input(ids.LINE_GRAPH_DROPDOWN, 'value'),
        Input(ids.TOP_BOTTOM_DROPDOWN, 'value'),
        Input(ids.LINE_GRAPH_NUMBER_RESTRICTION_DROPDOWN, 'value')])
def update_line_graph(metric, sorting_option, restriction_number):
    if metric is None or sorting_option is None or restriction_number is None:
        return html.Div([html.H3('Please choose from the two dropdowns to create a line graph to compare countries.')], style={'textAlign': 'center', 'margin-top': '50px', 'margin-bottom': '50px'})
    else:
        return line_graph.render_line_graph_country(metric, sorting_option, restriction_number)
        # return html.Div([html.H3('SELECTION')], style={'textAlign': 'center', 'margin-top': '50px', 'margin-bottom': '50px'})

# CALLBACK FOR THE CONTINENT LINE GRAPH
@app.callback(
    Output(ids.CONTINENT_LINE_GRAPH_CONTAINER, 'children'),
        [Input(ids.LINE_GRAPH_DROPDOWN, 'value')])
def update_continent_line_graph(metric):
    if metric is None:
        return None
    else:
        return line_graph.render_line_graph_continent(metric)


if __name__ == '__main__':
    app.run()
    # app.run_server(debug=True)