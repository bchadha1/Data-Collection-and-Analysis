import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import os
import pymongo
from pymongo import MongoClient
from datetime import datetime as dt

uri = "mongodb://127.0.0.1:27017/?compressors=zlib&readPreference=primary&gssapiServiceName=mongodb&appname=MongoDB" \
      "%20Compass&ssl=false"
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

    access_token = os.environ.get('620991207-TF2ni8UM9bYYdpV9UXkSsEankZhh1A603g8va0dl')
    access_secret = os.environ.get('VoHqILi4ZcWOX5ZsiYBxsVllFBdy3dFlDLD5VrNEcBgHV')
    consumer_key = os.environ.get('GcnhFpvaUhx8dr34vUXkRARHv')
    consumer_secret = os.environ.get('ZLfNDTIbMkV0dSueNI6joWzy1E0aoMtUIUbT1od2vhmQ5yV3kD')

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    twitter_stream = Stream(auth, TweetsListener())
    twitter_stream.filter(track=track, languages=['en'])
