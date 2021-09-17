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

server = app.server

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
                         {"label": 'UTC', "value": 'UTC'},
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
    html.H2("Viewership Distribution Between Games"),
    html.Div([
        "Games",
         dcc.Dropdown(id="select_games_pie",
                     options=[
                         {'label': x, 'value': x} for x in top_games],
                     multi=True,
                     value=top_games[:3],
                     style={'width': "100%"},
                     clearable=False
                 ),
    ]),
    html.Div([
        "Increment",
         dcc.Dropdown(id="select_increment_area",
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
    dcc.Graph(id='graph_pie', figure={}),
    dcc.Graph(id='graph_area', figure={}),
    
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
                     value=top_languages[:3],
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
    
    html.Br(),
    html.H2("Viewers Over Time By Game"),
    html.Div([
        "Games",
         dcc.Dropdown(id="select_games_votbg",
                     options=[
                         {'label': x, 'value': x} for x in top_games],
                     multi=True,
                     value=top_games[:3],
                     style={'width': "100%"},
                     clearable=False
                 ),
    ]),
    html.Div([
        "Increment",
         dcc.Dropdown(id="select_increment_votbg",
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
    dcc.Graph(id='graph_votbg', figure={}),

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    Output(component_id='graph_pie', component_property='figure'),
    Input(component_id='select_games_pie', component_property='value'),
)
def update_votbl(games):
    df = atlas_requests.top_games_by_views().reset_index()
    df['game'] = df['game'].apply(lambda x: x if (x in games) else 'Other')
    fig = px.pie(df, values='num_viewers', names='game', title='Average Distribution Past 7 Days')

    return fig

@app.callback(
    Output(component_id='graph_area', component_property='figure'),
    Input(component_id='select_games_pie', component_property='value'),
    Input(component_id='select_increment_area', component_property='value')
)
def update_votbl(games, increment):
    df = atlas_requests.total_views_per_increment_by_x(increment=increment)
    df.rename(columns = {'x':'game'}, inplace = True)
    df['game'] = df['game'].apply(lambda x: x if (x in games) else 'Other')
    df = df.groupby(['game','date']).sum().reset_index()
    df2 = atlas_requests.total_views_per_increment(increment=increment).set_index('date')['num_viewers'].to_dict()
    print(df)
    df['num_viewers_ratio'] = df.apply(lambda x: x['num_viewers']/df2[x['date']], axis=1)
    df.reset_index(inplace=True)
    df['game'] = pd.Categorical(df['game'], ['Other'] + games[::-1] )
    df.sort_values(['game','date'], inplace = True)
    fig = px.area(df, x="date", y="num_viewers_ratio", color='game', title='Distribution Over Time')

    return fig



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

@app.callback(
    Output(component_id='graph_votbg', component_property='figure'),
    Input(component_id='select_timezone', component_property='value'),
    Input(component_id='select_increment_votbg', component_property='value'),
    Input(component_id='select_games_votbg', component_property='value'),
)
def update_votbl(timezone, increment, games):
    df = atlas_requests.total_views_per_increment_by_x(increment, x='$game_name')
    df['date'] = df['date'].dt.tz_localize('UTC').dt.tz_convert(timezone)
    df.rename(columns = {'x':'game'}, inplace = True)
    fig = px.line(df[df['game'].isin(games)], x="date", y="num_viewers", color="game", labels={'date': '', 'num_viewers': ''})

    return fig



# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)