from pymongo import MongoClient
import csv
import os
from pathlib import Path

from app.config.settings import settings


NUMERIC_FIELDS = {
    "bedrooms",
    "bathrooms",
    "garage",
    "land_size_m2",
    "building_size_m2",
    "price_idr",
    "cluster",
    "pool",
    "mrt",
    "tol",
    "mall",
}


def get_collection():
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]
    return db[settings.MONGO_COLLECTION_NAME]


def _coerce_value(key, value):
    if value is None:
        return None

    cleaned_value = value.strip()
    if cleaned_value == "":
        return None

    if key in NUMERIC_FIELDS:
        try:
            if "." in cleaned_value or "e" in cleaned_value.lower():
                return float(cleaned_value)
            return int(cleaned_value)
        except ValueError:
            return cleaned_value

    return cleaned_value


def insert_csv_to_collection(csv_path=None, collection=None):
    """Insert rows from a CSV file into MongoDB using insert_many."""
    if collection is None:
        collection = get_collection()

    if csv_path is None:
        candidate_paths = [
            Path("data/raw/jakarta_properties_raw.csv"),
            Path("data/jakarta_properties_raw.csv"),
            Path("raw/jakarta_properties_raw.csv"),
        ]
        csv_path = None
        for path in candidate_paths:
            if path.exists():
                csv_path = path
                break

        if csv_path is None:
            raise FileNotFoundError("CSV file not found. Expected jakarta_properties_raw.csv in data/raw, data, or raw.")
    else:
        csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        records = []
        for row in reader:
            cleaned_row = {}
            for key, value in row.items():
                cleaned_row[key] = _coerce_value(key, value)
            records.append(cleaned_row)

    if not records:
        return {"inserted_count": 0, "file": str(csv_path)}

    result = collection.insert_many(records)
    return {"inserted_count": len(result.inserted_ids), "file": str(csv_path)}


if __name__ == "__main__":
    print(insert_csv_to_collection())


