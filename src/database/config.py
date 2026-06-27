from pymongo import MongoClient
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["jakarta_properties"]
coll = db['properties']



