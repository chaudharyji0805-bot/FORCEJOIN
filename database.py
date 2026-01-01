from pymongo import MongoClient
from config import MONGO_URI

mongo = MongoClient(MONGO_URI)
db = mongo.forcejoinbot

# collections
users = db.users                 # all users (private + group)
group_channels = db.group_channels  # per-group force join
