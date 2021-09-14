import datetime
import pandas as pd
from pymongo import MongoClient



client = MongoClient("mongodb+srv://read-only:EzWvxGgSDOIX2T9o@cluster0.chzpe.mongodb.net/?retryWrites=true&w=majority")
db = client.twitch_dashboard
streams = db.streams

def total_views_per_increment(increment='T', days=7):
    pipeline = [
        {'$match': {'date': {'$gt': (datetime.datetime.utcnow() - datetime.timedelta(days=days))}}},
         {'$group': {'_id': '$date', 
                    'num_viewers': {'$sum': '$viewer_count'}}},
        {'$project': {'_id': 0, 'num_viewers': 1, 'date': '$_id'}},
        {'$sort': {'num_viewers': -1}},
    ]

    response = list(streams.aggregate(pipeline))
    df = pd.DataFrame(response)#.set_index('game')
    df['date'] = df['date'].dt.floor(increment)
    df = df.groupby('date').sum().reset_index()
    return df

# Top games by total views past week
def top_games_by_views(days=7):
    pipeline = [

        {'$match': {'date': {'$gt': (datetime.datetime.utcnow() - datetime.timedelta(days=days))}}},
        {'$group': {'_id': '$game_name', 
                    'num_viewers': {'$sum': '$viewer_count'}}},
        {'$project': {'_id': 0, 'game': '$_id', 'num_viewers': 1}},
        {'$sort': {'num_viewers': -1}},
    ]

    response = list(streams.aggregate(pipeline))
    df = pd.DataFrame(response).set_index('game')
    return df

def total_views_per_increment_by_x(increment='T', x='$game_name'):
    pipeline = [
        {'$group': {'_id': {'date': '$date', 'x':x}, 
                    'num_viewers': {'$sum': '$viewer_count'}, 
                    'date': {'$first': '$date'}, 
                    'x': {'$first': x}}},
        {'$project': {'_id': 0, 'num_viewers': 1, 'date': 1, 'x': 1}},
        {'$sort': {'date': 1}}
    ]

    response = list(streams.aggregate(pipeline))
    df = pd.DataFrame(response)
    df['date'] = df['date'].dt.floor(increment)
    df = df.groupby(['date','x']).sum().reset_index()
    return df


def top_languages_by_views(days=7):
    pipeline = [

        {'$match': {'date': {'$gt': (datetime.datetime.utcnow() - datetime.timedelta(days=days))}}},
        {'$group': {'_id': '$language', 
                    'num_viewers': {'$sum': '$viewer_count'}}},
        {'$project': {'_id': 0, 'language': '$_id', 'num_viewers': 1}},
        {'$sort': {'num_viewers': -1}},
    ]

    response = list(streams.aggregate(pipeline))
    df = pd.DataFrame(response).set_index('language')
    return df