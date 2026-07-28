import numpy as np
import pandas as pd
import joblib
import json
from app.config.settings import settings
from app.ml.preprocessing import transform_feature

class Predictor:
    def __init__(self):
        self.model = joblib.load(settings.MODEL_PATH)
        self.encoder_district = joblib.load(settings.ENCODER_DISTRICT_PATH)
        self.encoder_subdistrict = joblib.load(settings.ENCODER_SUBDISTRICT_PATH)
        with open(settings.METRICS_PATH) as file:
            self.metrics = json.load(file)

    def predict(self, data):
        df = pd.DataFrame([data])

        # Log transform
        df = transform_feature(df)

        # One-Hot Encoding city
        feature = list(self.model.feature_names_in_)
        city_cols = [c for c in feature if c.startswith('city_')]
        for col in city_cols:
            df[col] = 0
        city_key = f"city_{data['city']}"
        if city_key in city_cols:
            df[city_key] = 1
        df = df.drop(columns=["city"], errors="ignore")

        # Target Encoding district
        df["district"] = self.encoder_district.transform(df[["district"]]).flatten()
        df["sub_district"] = self.encoder_subdistrict.transform(df[["sub_district"]]).flatten()

        # Prediksi
        df        = df[self.model.feature_names_in_]
        price_log = self.model.predict(df)[0]
        price     = np.expm1(price_log)

        # Rentang harga     
        margin = price * self.metrics["MAPE"]
        return {
            "price":      round(price),
            "price_low":  round(price - margin),
            "price_high": round(price + margin),
        }


predictor = Predictor()