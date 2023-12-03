import sys
from pymongo import MongoClient

port = int(sys.argv[1])
client = MongoClient('localhost', port)

db = client["A4dbEmbed"]
SongwritersRecordings = db["SongwritersRecordings"]

pipe = [
    {"$unwind": "$recordings"},
    {"$group": {
        "_id": "$songwriter_id",
        "total_length": {"$sum": "$recordings.length"},
        "songwriter_id": {"$first": "$songwriter_id"}
    }},
]

data1 = SongwritersRecordings.aggregate(pipeline = pipe)
data = list(data1)

for document in data:
    print(document)