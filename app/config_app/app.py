from config.base import BaseConfig
from pathlib import Path

class ApiConfig(BaseConfig):
    # Tambahan khusus FastAPI
    MODEL_PATH: Path = BaseConfig().BASE_DIR / "artifacts" / "models" / "pipeline_model.pkl"
    METRICS_PATH: Path = BaseConfig().BASE_DIR / "artifacts" / "metrics" / "metrics.json"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

settings = ApiConfig()