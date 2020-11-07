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
