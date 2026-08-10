import json
from pathlib import Path

import numpy as np
import pandas as pd
from ml.config_ml.ml import settings
from database.loader import DatasetLoader


class Preprocessing:
    """Preprocessing pipeline dengan state di instance (df, mapping, path)."""

    def __init__(
        self,
        mapping_path: str = settings.DISTRICT_MAPPING_PATH,
        log_unknown_path: str = "log/unknown_district.log",
        city_path: str = settings.CITY_MAPPING_PATH,
        refresh: bool = False,
    ):
        self.mapping_path = mapping_path
        self.log_unknown_path = log_unknown_path
        self.city_path = city_path
        self.refresh = refresh

        self.df: pd.DataFrame | None = None
        self.mapping: dict | None = None

    def load_dataset(self):
        self.df = DatasetLoader.load_dataset(refresh=self.refresh)
        return self.df

    def standard(self):
        self.df["price_idr"] = pd.to_numeric(self.df["price_idr"], errors="coerce")
        self.df["garage"] = self.df["garage"].fillna(0)
        self.df["title"] = self.df["title"].str.lower()
        return self.df

    def filtering(self):
        map_col = ["bedrooms", "bathrooms", "garage"]
        for col in map_col:
            self.df = self.df[
                (self.df[col] != self.df["land_size_m2"])
                & (self.df[col] != self.df["building_size_m2"])
            ]
        self.df = self.df[
            (self.df["price_idr"] > 0)
            & (self.df["bedrooms"] > 0)
            & (self.df["bathrooms"] > 0)
        ]
        self.df = self.df[
            (self.df["building_size_m2"] >= 30) & (self.df["land_size_m2"] >= 30)
        ]
        self.df = self.df[
            (self.df["bedrooms"] <= 30)
            & (self.df["bathrooms"] <= 30)
            & (self.df["garage"] <= 30)
        ]
        self.df = self.df.dropna(axis=0)
        self.df = self.df[(self.df["rumah_sakit"] == 0) & (self.df["kos"] == 0)]
        price_per_m2 = self.df["price_idr"] / self.df["land_size_m2"]
        self.df = self.df[
            (price_per_m2 >= 1_000_000) & (price_per_m2 <= 150_000_000)
        ]
        lower = self.df["price_idr"].quantile(0.1)
        upper = self.df["price_idr"].quantile(0.99)
        self.df = self.df[
            (self.df["price_idr"] >= lower) & (self.df["price_idr"] <= upper)
        ]
        return self.df

    def feature(self):
        self.df["cluster"] = self.df["title"].str.contains(
            "cluster", na=False
        ).astype(int)
        self.df["pool"] = self.df["title"].str.contains(
            r"kolam renang|pool", na=False
        ).astype(int)
        self.df["mrt"] = self.df["title"].str.contains(
            r"mrt", na=False
        ).astype(int)
        self.df["tol"] = self.df["title"].str.contains(
            r"tol", na=False
        ).astype(int)
        self.df["mall"] = self.df["title"].str.contains(
            r"mall", na=False
        ).astype(int)
        self.df["kos"] = self.df["title"].str.contains(
            r"kos|kost|kostan|kosan", na=False
        ).astype(int)
        self.df["rumah_sakit"] = (
            self.df["title"].str.contains(r"rumah sakit", na=False)
            & ~self.df["title"].str.contains(
                r"dekat|near|sekitar|selangkah", na=False
            )
        ).astype(int)
        return self.df

    def transform_feature(self):
        self.df["land_size_m2"] = np.log1p(self.df["land_size_m2"])
        self.df["building_size_m2"] = np.log1p(self.df["building_size_m2"])
        return self.df

    def transform_target(self) -> pd.DataFrame:
        self.df["price_idr"] = np.log1p(self.df["price_idr"])
        return self.df

    def encode(self) -> pd.DataFrame:
        self.df = pd.get_dummies(self.df, columns=["city"], dtype=int)
        return self.df

    def drop(self) -> pd.DataFrame:
        self.df = self.df.drop(columns=["title", "scraped_at", "rumah_sakit", "kos"])
        return self.df

    def district_mapping(self):
        with open(self.mapping_path, "r") as file:
            self.mapping = json.load(file)

        self.df["district"] = self.df["district"].str.lower()
        self.df["sub_district"] = self.df["district"].copy()
        unknown = set(
            self.df[~self.df["sub_district"].isin(self.mapping.keys())][
                "sub_district"
            ].unique()
        )

        if len(unknown) > 0:
            print(f"{len(unknown)} sub district tidak ada di mapping:")
            for d in sorted(unknown):
                print(f" - '{d}'")

        log_unknown = Path(self.log_unknown_path)
        logged = set()
        if log_unknown.exists():
            with open(log_unknown, "r") as file:
                logged = {i.strip() for i in file}

        new_unknown = unknown - logged
        if new_unknown:
            with open(log_unknown, "a") as file:
                for d in sorted(new_unknown):
                    file.write(f"{d}\n")

        self.df["district"] = self.df["district"].map(self.mapping)
        return self.df

    def run(self):
        # Jalankan full preprocessing pipeline
        print("Load Dataset...")
        self.load_dataset()
        print("Done Load Dataset...")
        self.standard()
        self.feature()
        self.filtering()
        self.transform_feature()
        self.transform_target()
        self.encode()
        self.drop()
        self.district_mapping()
        print("Cleaning Done...")
        return self.df

    def save(
        self,
        path: str = "dataset/processed/jakarta_properties_processed.csv",
    ):
        if self.df is None:
            raise ValueError("DataFrame kosong. Jalankan run() dulu sebelum save().")
        self.df.to_csv(path, index=False)


def pipeline():
    return Preprocessing().run()


def save(df: pd.DataFrame):
    df.to_csv("dataset/processed/jakarta_properties_processed.csv", index=False)


if __name__ == "__main__":
    preprocessor = Preprocessing()
    df = preprocessor.run()
    preprocessor.save(df)
