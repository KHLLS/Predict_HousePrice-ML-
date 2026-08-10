import pandas as pd
from pymongo import MongoClient
from config.base import settings


def get_collection():
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]

    return db[settings.MONGO_COLLECTION_NAME]


