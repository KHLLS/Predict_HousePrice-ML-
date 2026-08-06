from pymongo import MongoClient
from config.settings import settings

client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)
print(client.admin.command("ping"))