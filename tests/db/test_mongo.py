from pymongo import MongoClient
from database.config_db import settings

client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)
print(client.admin.command("ping"))