import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import atlas_requests

import datetime

app = dash.Dash(__name__)

top_languages = atlas_requests.top_languages_by_views().index
top_games = atlas_requests.top_games_by_views().index



# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Twitch Dashboard", style={'text-align': 'center'}),
    
    html.H3("Global Settings"),
    html.Div([
        "Timezone",
         dcc.Dropdown(id="select_timezone",
                     options=[
                         {"label": 'US/Pacific', "value": 'US/Pacific'},
                         {"label": 'US/Central', "value": 'US/Central'},
                         {"label": 'US/Eastern', "value": 'US/Eastern'},
                         {"label": 'Europe/London', "value": 'Europe/London'}],
                     multi=False,
                     value='Europe/London',
                     style={'width': "40%"},
                     clearable=False
                 ),
    ]),
   

    html.Br(),
    html.H2("Viewers Over Time"),
    html.Div([
        "Increment",
         dcc.Dropdown(id="select_increment_vot",
                     options=[
                         {"label": 'Half-Hourly', "value": 'T'},
                         {"label": 'Hourly', "value": 'H'},
                         {"label": 'Daily', "value": 'D'}],
                     multi=False,
                     value='T',
                     style={'width': "40%"},
                     clearable=False
                 ),
    ]),
    dcc.Graph(id='graph_vot', figure={}),
    
    html.Br(),
    html.H2("Viewers Over Time By Language"),
    html.Div([
        "Languages",
         dcc.Dropdown(id="select_languages_votbl",
                     options=[
                         {'label': x, 'value': x} for x in top_languages],
                     multi=True,
                     value=top_languages[:5],
                     style={'width': "40%"},
                     clearable=False
                 ),
    ]),
    html.Div([
        "Increment",
         dcc.Dropdown(id="select_increment_votbl",
                     options=[
                         {"label": 'Half-Hourly', "value": 'T'},
                         {"label": 'Hourly', "value": 'H'},
                         {"label": 'Daily', "value": 'D'}],
                     multi=False,
                     value='T',
                     style={'width': "40%"},
                     clearable=False
                 ),
    ]),
    dcc.Graph(id='graph_votbl', figure={}),

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
     Output(component_id='graph_vot', component_property='figure'),
     Input(component_id='select_timezone', component_property='value'),
     Input(component_id='select_increment_vot', component_property='value')
)
def update_vot(timezone, increment):
    df = atlas_requests.total_views_per_increment(increment)
    df['date'] = df['date'].dt.tz_localize('UTC').dt.tz_convert(timezone)

    fig = px.line(df, x="date", y="num_viewers", labels={'date': '', 'num_viewers': ''})

    return fig



@app.callback(
    Output(component_id='graph_votbl', component_property='figure'),
    Input(component_id='select_timezone', component_property='value'),
    Input(component_id='select_increment_votbl', component_property='value'),
    Input(component_id='select_languages_votbl', component_property='value'),
)
def update_votbl(timezone, increment, languages):
    df = atlas_requests.total_views_per_increment_by_x(increment, x='$language')
    df['date'] = df['date'].dt.tz_localize('UTC').dt.tz_convert(timezone)
    df.rename(columns = {'x':'language'}, inplace = True)
    fig = px.line(df[df['language'].isin(languages)], x="date", y="num_viewers", color="language", labels={'date': '', 'num_viewers': ''})

    return fig



# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)