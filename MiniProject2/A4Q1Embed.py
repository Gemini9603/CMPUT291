import sys
from pymongo import MongoClient

port = int(sys.argv[1])
client = MongoClient('localhost', port)

db = client["A4dbEmbed"]
SongwritersRecordings = db["SongwritersRecordings"]

pipe = [
    {"$project": {
        "_id": "$_id",
        "songwriter_id": "$songwriter_id",
        "name": "$name",
        "num_recordings": {"$size": "$recordings"}
    }},
    {"$match": {"num_recordings": {"$gte": 1}}}
]

data1 = SongwritersRecordings.aggregate(pipeline = pipe)
data = list(data1)

for document in data:
    print(document)