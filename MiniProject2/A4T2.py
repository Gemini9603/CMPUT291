import sys
import json
from bson import Binary, Code
from bson.json_util import dumps
from bson.json_util import loads
from pymongo import MongoClient

port = int(sys.argv[1])
client = MongoClient('localhost', port)

db = client["A4dbEmbed"]

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
if "Recordings" in collist:
    print("The collection exists.")

Recordings = db["Recordings"]
Recordings.delete_many({})

with open('recordings.json', encoding="utf-8") as file:
    file_data = json.load(file)
data1 = dumps(file_data)
data = loads(data1)
Recordings.insert_many(data)

collist = db.list_collection_names()
if "SongwritersRecordings" in collist:
    print("The collection exists.")

SongwritersRecordings = db["SongwritersRecordings"]
SongwritersRecordings.delete_many({})

pipe = [
    {"$unwind": "$recordings"},
    {"$lookup": {
        "from": "Recordings",
        "localField": "recordings",
        "foreignField": "recording_id",
        "as": "SongwritersRecordings"
    }},
    {"$unwind": "$SongwritersRecordings"},
    {"$group": {
        "_id": "$_id",
        "songwriter_id": {"$first": "$songwriter_id"},
        "fans": {"$first": "$fans"},
        "name": {"$first": "$name"},
        "reputation": {"$first": "$reputation"},
        "genres": {"$first": "$genres"},
        "recordings": {"$push": "$SongwritersRecordings"}
    }}
]

data1 = songwriters.aggregate(pipeline = pipe)
data = list(data1)
SongwritersRecordings.insert_many(data)

pipe = [{"$match":{
    "recordings": {"$size": 0}
    }}
]
data1 = songwriters.aggregate(pipeline = pipe)
data = list(data1)
SongwritersRecordings.insert_many(data)

db.songwriters.drop()
db.Recordings.drop()