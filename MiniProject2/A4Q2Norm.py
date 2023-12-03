import sys
from pymongo import MongoClient

port = int(sys.argv[1])
client = MongoClient('localhost', port)

db = client["A4dbNorm"]
recordings = db["recordings"]

pipe = [
    {"$match": {"recording_id": {"$regex": "^70"}}},
    {"$group": {
        "_id": "",
        "avg_rhythmicality": {"$avg": "$rhythmicality"}
    }}
]

data1 = recordings.aggregate(pipeline = pipe)
data = list(data1)

for document in data:
    print(document)