import json
import os
import pymongo
from pymongo import MongoClient
from datetime import datetime as dt

uri = "mongodb://127.0.0.1:27017/?compressors=zlib&readPreference=primary&gssapiServiceName=mongodb&appname=MongoDB" \
      "%20Compass&ssl=false "
client = pymongo.MongoClient(uri)
db = client.test
collection = db['Twitter Data']

def stream_generator(text):
    dic = []
    for tweet in text.items():
        dic.append(tweet)
    yield dic


class TweetsListener(StreamListener):

    def on_data(self, data):
        try:
            tweet = json.loads(data)
            st = stream_generator(tweet)
            for x in st:
                collection.insert_one({'_id': dt.now(), 'tweets': x})
                print('Inserting...')
            return True
        except BaseException as e:
            print(e)
        return True


if __name__ == "__main__":
    track = ['trump', 'MAGA', 'trump2020', '#MAGA', 'thedonald', 'bitcoin', 'ripple']

    access_token = os.environ.get('ACCESS_TOKEN')
    access_secret = os.environ.get('ACCESS_SECRET')
    consumer_key = os.environ.get('CONSUMER_KEY')
    consumer_secret = os.environ.get('CONSUMER_SECRET')

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    twitter_stream = Stream(auth, TweetsListener())
    twitter_stream.filter(track=track, languages=['en'])
