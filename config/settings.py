import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")


class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI", "")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "jakarta_properties")
    MONGO_COLLECTION_NAME: str = os.getenv("MONGO_COLLECTION_NAME", "properties")
    MLFLOW_TRACKING_URI: str = os.getenv("MLFLOW_TRACKING_URI","")
    MLFLOW_EXPERIMENT_NAME: str = os.getenv("MLFLOW_EXPERIMENT_NAME","")
    MLFLOW_RUN_ID_MODEL: str = os.getenv("MLFLOW_RUN_ID_MODEL", "")
    MLFLOW_RUN_ID_METRIC: str = os.getenv("MLFLOW_RUN_ID_METRIC", "")
    MLFLOW_MODEL_NAME: str = os.getenv("MLFLOW_MODEL_NAME","")

settings = Settings()
