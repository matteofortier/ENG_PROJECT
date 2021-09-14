# %pip install pymongo
# %pip install python-twitch-client
# %pip install apscheduler
import time
import datetime
import twitch_to_mongo
import twitch
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler

mongo_client = None
mongo_db = None
twitch_client = None

def refresh():
    global mongo_client, mongo_db, twitch_client
    mongo_client = MongoClient(
        "mongodb+srv://matteofortier:CPm2bCTBmHsP8MqF@cluster0.chzpe.mongodb.net/?retryWrites=true&w=majority"
    )
    mongo_db = mongo_client.twitch_dashboard
    twitch_client = twitch_to_mongo.twitch_client()
    
def job():
    current_time = datetime.datetime.utcnow()
    refresh()
    print('Pulling from Twitch API -> Mongo Atlas')
    twitch_to_mongo.update_mongo(mongo_db.streams, twitch_client, n_streams=1000, date=current_time)
    
sched = BackgroundScheduler(daemon=True)
sched.add_job(job,
              'interval',
              minutes=30, 
              start_date='2021-09-10 23:30:00', 
              end_date='2021-09-19 00:00:00')

sched.start()

try:
    # This is here to simulate application activity (which keeps the main thread alive).
    while True:
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    # Not strictly necessary if daemonic mode is enabled but should be done if possible
#     sched.shutdown()
    pass