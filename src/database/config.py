from pymongo import MongoClient
import pandas as pd

client = MongoClient('mongodb://localhost:27017')
db = client["jakarta_properties"]
coll = db['properties']

