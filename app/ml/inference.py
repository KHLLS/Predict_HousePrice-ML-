import numpy as np
import pandas as pd
import joblib
import json
from app.config.settings import settings
from app.ml.preprocessing import transform_feature

class Predictor:
    def __init__(self):
        self.pipeline = joblib.load(settings.MODEL_PATH)
        with open(settings.METRICS_PATH) as file:
            self.metrics = json.load(file)

    def predict(self, data):
        df = pd.DataFrame([data])

        # Log transform
        df = transform_feature(df)

        # One-Hot Encoding city
        feature = list(self.pipeline.feature_names_in_)
        city_cols = [c for c in feature if c.startswith('city_')]
        for col in city_cols:
            df[col] = 0
        city_key = f"city_{data['city']}"
        if city_key in city_cols:
            df[city_key] = 1
        df = df.drop(columns=["city"], errors="ignore")

        # Urutan dan seluruh kolom harus sama seperti data training
        df = df.reindex(
            columns=self.pipeline.feature_names_in_,
            fill_value=0
        )

        # Pipeline otomatis melakukan Target Encoding lalu prediksi        price_log = self.pipeline.predict(df)[0]
        price     = np.expm1(price_log)

        # Rentang harga     
        margin = price * self.metrics["MAPE"]
        return {
            "price":      round(price),
            "price_low":  round(price - margin),
            "price_high": round(price + margin),
        }


predictor = Predictor()