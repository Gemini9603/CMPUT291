import sys
import json
from bson import Binary, Code
from bson.json_util import dumps
from bson.json_util import loads
from pymongo import MongoClient

port = int(sys.argv[1])
client = MongoClient('localhost', port)

db = client["A4dbNorm"]

collist = db.list_collection_names()
if "songwriters" in collist:
    print("The collection exists.")

songwriters = db["songwriters"]
songwriters.delete_many({})

with open('songwriters.json', encoding="utf-8") as file:
    file_data = json.load(file)
data1 = dumps(file_data)
data = loads(data1)
songwriters.insert_many(data)

collist = db.list_collection_names()
if "recordings" in collist:
    print("The collection exists.")

recordings = db["recordings"]
recordings.delete_many({})

with open('recordings.json', encoding="utf-8") as file:
    file_data = json.load(file)
data1 = dumps(file_data)
data = loads(data1)
recordings.insert_many(data)