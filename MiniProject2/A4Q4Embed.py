import sys
from datetime import datetime
from pymongo import MongoClient

port = int(sys.argv[1])
client = MongoClient('localhost', port)

db = client["A4dbEmbed"]
SongwritersRecordings = db["SongwritersRecordings"]

issued = datetime(1950, 1, 1, 0, 0)

pipe = [
    {"$unwind": "$recordings"},
    {"$match": {"recordings.issue_date": {"$gte": issued}}},
    {"$project": {
        "_id": "$_id",
        "name": "$name",
        "r_name": "$recordings.name",
        "r_issue_date": "$recordings.issue_date"
    }}
]

data1 = SongwritersRecordings.aggregate(pipeline = pipe)
data = list(data1)

for document in data:
    print(document)