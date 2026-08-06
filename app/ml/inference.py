import numpy as np
import pandas as pd
from app.ml.preprocessing import transform_feature
from mlflow_utils.loader import loader
import os

class Predictor:
    def __init__(self):
        # Prevent MLflow connection in test environment
        if os.getenv("TESTING") == "true":
            self.pipeline = None
            self.metrics = {"test_mape": 0.2}
        else:
            self.pipeline = loader.load_model()
            self.metrics = loader.get_metrics()

    def predict(self, data):
        if self.pipeline is None:
            # Fallback for tests
            return {
                "price": 1000000,
                "price_low": 800000,
                "price_high": 1200000,
            }
            
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

        # Pipeline otomatis melakukan Target Encoding lalu prediksi
        price_log = self.pipeline.predict(df)[0]
        price     = np.expm1(price_log)

        # Rentang harga     
        margin = price * self.metrics['test_mape']
        return {
            "price":      round(price),
            "price_low":  round(price - margin),
            "price_high": round(price + margin),
        }


predictor = Predictor()