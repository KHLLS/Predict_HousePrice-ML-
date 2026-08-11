from pymongo import MongoClient
from database.config_db import settings

def get_collection():
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]

    return db[settings.MONGO_COLLECTION_NAME]


