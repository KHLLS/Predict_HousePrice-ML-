from config.base import BaseConfig
from pathlib import Path

class MLConfig(BaseConfig):
    # Tambahan khusus MLops
    MLFLOW_TRACKING_URI: str = "http://localhost:5000"
    MLFLOW_MODEL_NAME: str = "harga-rumah-jakarta"
    MLFLOW_EXPERIMENT_NAME: str = "prediksi-harga"


settings = MLConfig()