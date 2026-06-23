import numpy as np
import pandas as pd
import joblib
import json

class Predictor:
    def __init__(self):
        self.model   = joblib.load("models/model.pkl")
        self.encoder = joblib.load("models/encoder/encoder.pkl")
        with open("models/metrics_model.json") as file:
            self.metrics = json.load(file)

    def predict(self, data):
        df = pd.DataFrame([data])

        # Log transform
        df["land_size_m2"]     = np.log1p(df["land_size_m2"])
        df["building_size_m2"] = np.log1p(df["building_size_m2"])

        # One-Hot Encoding city
        city_cols = [
            "city_Jakarta Barat",
            "city_Jakarta Pusat",
            "city_Jakarta Selatan",
            "city_Jakarta Timur",
            "city_Jakarta Utara",
        ]
        for col in city_cols:
            df[col] = 0
        city_key = f"city_{data['city']}"
        if city_key in city_cols:
            df[city_key] = 1
        df = df.drop(columns=["city"], errors="ignore")

        # Target Encoding district
        df["district"] = self.encoder.transform(df[["district"]]).flatten()

        # Prediksi
        df        = df[self.model.feature_names_in_]
        price_log = self.model.predict(df)[0]
        price     = np.expm1(price_log)

        # Rentang harga dari median error historis (Q50)
        margin = price * self.metrics["Q50"]
        return {
            "price":      round(price),
            "price_low":  round(price - margin),
            "price_high": round(price + margin),
        }


predictor = Predictor()
