import pandas as pd
from pymongo import MongoClient
from config.settings import settings


def get_collection():
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]

    return db[settings.MONGO_COLLECTION_NAME]


def insert_csv_to_collection(csv_path):
    collection = get_collection()

    df = pd.read_csv(csv_path)

    df = df.where(pd.notnull(df), None)

    data = df.to_dict("records")

    if not data:
        return 0

    result = collection.insert_many(data)

    return len(result.inserted_ids)

if __name__ == "__main__":
    print(insert_csv_to_collection("data/raw/jakarta_properties_raw.csv"))