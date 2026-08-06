from pymongo import MongoClient
import csv
from pathlib import Path
from typing import Any, Dict, Optional, Union

from config.settings import settings


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


def _coerce_value(key: str, value: Optional[str]) -> Optional[Union[int, float, str]]:
    if not value or not (cleaned := value.strip()):
        return None

    if key in NUMERIC_FIELDS:
        try:
            return float(cleaned) if "." in cleaned or "e" in cleaned.lower() else int(cleaned)
        except ValueError:
            return cleaned

    return cleaned


def insert_csv_to_collection(csv_path: Optional[Union[str, Path]] = None, collection=None) -> Dict[str, Any]:
    """Mengimpor baris dari file CSV ke dalam koleksi MongoDB."""
    if collection is None:
        collection = get_collection()

    if csv_path is None:
        candidate_paths = [
            Path("data/raw/jakarta_properties_raw.csv"),
            Path("data/jakarta_properties_raw.csv"),
            Path("raw/jakarta_properties_raw.csv"),
        ]
        csv_path = next((p for p in candidate_paths if p.exists()), None)
        if csv_path is None:
            raise FileNotFoundError(
                "File CSV tidak ditemukan. Harapkan jakarta_properties_raw.csv di data/raw, data, atau raw."
            )
    else:
        csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"File CSV tidak ditemukan: {csv_path}")

    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        records = [
            {key: _coerce_value(key, value) for key, value in row.items()}
            for row in reader
        ]

    if not records:
        return {"inserted_count": 0, "file": str(csv_path)}

    result = collection.insert_many(records)
    return {"inserted_count": len(result.inserted_ids), "file": str(csv_path)}


if __name__ == "__main__":
    print(insert_csv_to_collection())


