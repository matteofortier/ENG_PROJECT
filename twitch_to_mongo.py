import twitch
import datetime
from itertools import islice
from pymongo import MongoClient

def twitch_client():
    twitch_client = twitch.TwitchHelix(
        client_id='efo5rjmg6na3wpjs5ciptmnzx6p4bs',
        client_secret='w1irngceaw9sblt7xk00z5dvt2f2eu',
        scopes=[twitch.constants.OAUTH_SCOPE_ANALYTICS_READ_EXTENSIONS]
    )
    twitch_client.get_oauth()
    return twitch_client

def add_date(document, date):
    document.update({'date': date})
    return document

def top_streams(twitch_client, n_streams, date):
    response = twitch_client.get_streams(page_size=100)
    streams_iterator = islice(response, 0, n_streams)
    return [dict(add_date(stream, date)) for stream in streams_iterator]

def update_mongo(mongo_collection, twitch_client, n_streams=1000, date=datetime.datetime.utcnow()):
    mongo_collection.insert_many(top_streams(twitch_client, n_streams, date),ordered=False)