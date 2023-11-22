import sys
from datetime import datetime
from pymongo import MongoClient

port = int(sys.argv[1])
client = MongoClient('localhost', port)

db = client["A4dbNorm"]
songwriters = db["songwriters"]
recordings = db["recordings"]

issued = datetime(1950, 1, 1, 0, 0)
pipe = [
    {"$match": {"issue_date": {"$gte": issued}}},
    {"$unwind": "$songwriter_ids"},
    {"$lookup": {
        "from": "songwriters",
        "localField": "songwriter_ids",
        "foreignField": "songwriter_id",
        "as": "songwriter"
    }},
    {"$unwind": "$songwriter"},
    {"$project": {
        "_id": "$songwriter._id",
        "name": "$songwriter.name",
        "r_name": "$name",
        "r_issue_date": "$issue_date"
    }}
]

data1 = recordings.aggregate(pipeline = pipe)
data = list(data1)

for document in data:
    print(document)