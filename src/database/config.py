from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["jakarta_properties"]
coll = db['properties']


