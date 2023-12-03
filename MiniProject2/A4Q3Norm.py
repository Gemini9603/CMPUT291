import sys
from pymongo import MongoClient

port = int(sys.argv[1])
client = MongoClient('localhost', port)

db = client["A4dbNorm"]
songwriters = db["songwriters"]
recordings = db["recordings"]

pipe = [
    {"$unwind": "$recordings"},
    {"$lookup": {
        "from": "recordings",
        "localField": "recordings",
        "foreignField": "recording_id",
        "as": "SongwritersRecordings"
    }},
    {"$unwind": "$SongwritersRecordings"},
    {"$group": {
        "_id": "$songwriter_id",
        "total_length": {"$sum": "$SongwritersRecordings.length"},
        "songwriter_id": {"$first": "$songwriter_id"}
    }}
]

data1 = songwriters.aggregate(pipeline = pipe)
data = list(data1)

for document in data:
    print(document)