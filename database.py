from pymongo import MongoClient
from config import MONGO_URI

mongo = MongoClient(MONGO_URI)
db = mongo.forcejoinbot

users = db.users

group_settings = db.group_settings
# example document:
# {
#   group_id: -100123,
#   enabled: true,
#   admins: [12345, 67890],
#   channels: [
#       {username: "ch1", invite: "..."},
#       {username: "ch2", invite: None}
#   ]
# }
