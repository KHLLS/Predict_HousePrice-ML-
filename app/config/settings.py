import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")


class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI", "")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "jakarta_properties")
    MONGO_COLLECTION_NAME: str = os.getenv("MONGO_COLLECTION_NAME", "properties")
    MODEL_PATH: str = os.getenv("MODEL_PATH", "artifacts/models/model.pkl")
    METRICS_PATH: str = os.getenv("METRICS_PATH", "artifacts/models/metrics_model.json")


settings = Settings()
