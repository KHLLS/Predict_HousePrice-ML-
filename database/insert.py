import pandas as pd
from database.client import get_collection
from database.config_db import settings

def insert_csv_to_collection(csv_path):
    collection = get_collection()

    df = pd.read_csv(csv_path)

    data = (
        df.astype(object)
        .where(pd.notnull(df), None)
        .to_dict("records")
    )

    if not data:
        return 0

    result = collection.insert_many(data)

    return len(result.inserted_ids)

if __name__ == "__main__":
    print(insert_csv_to_collection(settings.RAW_DATASET))