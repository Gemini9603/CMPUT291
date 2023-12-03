import sys
from pymongo import MongoClient

port = int(sys.argv[1])
client = MongoClient('localhost', port)

db = client["A4dbEmbed"]
SongwritersRecordings = db["SongwritersRecordings"]

pipe = [
    {"$unwind": "$recordings"},
    {"$match": {"recordings.recording_id": {"$regex": "^70"}}},
    {"$group": {
        "_id": "",
        "avg_rhythmicality": {"$avg": "$recordings.rhythmicality"}
    }}
]

data1 = SongwritersRecordings.aggregate(pipeline = pipe)
data = list(data1)

for document in data:
    print(document)