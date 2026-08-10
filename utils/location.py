import json

import pandas as pd

from app.core.inference import predictor
from config.base import settings


def load_city():
    if predictor.pipeline is None:
        return [
            "Jakarta Pusat",
            "Jakarta Selatan",
            "Jakarta Timur",
            "Jakarta Barat",
            "Jakarta Utara",
        ]

    features = list(predictor.pipeline.feature_names_in_)
    city_map = [
        c.removeprefix("city_")
        for c in features
        if c.startswith("city_")
    ]

    with open(settings.CITY_MAPPING_PATH, "w", encoding="utf-8") as f:
        json.dump(city_map, f, indent=4, ensure_ascii=False)

    return city_map


def load_district_map():
    with open(settings.DISTRICT_MAPPING_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_districts_by_city():
    df = pd.read_csv(settings.PROCESSED_DATA_PATH)

    city_cols = [c for c in df.columns if c.startswith("city_")]

    df = df[["district", *city_cols]].dropna(subset=["district"])
    df["district"] = df["district"].str.strip().str.lower()
    df["city"] = df[city_cols].idxmax(axis=1).str.removeprefix("city_")

    districts_by_city = (
        df.groupby("city")["district"]
        .apply(lambda s: sorted(s.unique()))
        .to_dict()
    )

    with open(settings.DISTRICTS_BY_CITY_PATH, "w", encoding="utf-8") as f:
        json.dump(districts_by_city, f, indent=4, ensure_ascii=False)

    return districts_by_city


if __name__ == "__main__":
    extract_districts_by_city()
