from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class BaseConfig(BaseSettings):
    BASE_DIR: Path = Path(__file__).parent.parent.resolve()
    # Path — shared
    REFERENCES_DIR: Path = BASE_DIR / "reference"
    DATASET_DIR : Path = BASE_DIR / "ml" / "dataset"
    CITY_MAPPING_PATH: Path = REFERENCES_DIR / "city_mapping.json"
    DISTRICT_MAPPING_PATH: Path = REFERENCES_DIR / "district_mapping.json"
    DISTRICT_BY_CITY: Path = REFERENCES_DIR / "districts_by_city.json"
    PROCESSED_DATASET : Path = DATASET_DIR / "processed" / "jakarta_properties_processed.csv"
    RAW_DATASET : Path = DATASET_DIR / "raw" / "jakarta_properties_raw.csv"

    # MongoDB — shared
    MONGO_URI : str
    MONGO_DB_NAME :str
    MONGO_COLLECTION_NAME :str

    model_config = ConfigDict(
        extra="ignore",
        env_file=str(BASE_DIR / ".env")
    )

settings = BaseConfig()
#     # Mongo
#     MONGO_URI: str
#     MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "jakarta_properties")
#     MONGO_COLLECTION_NAME: str = os.getenv("MONGO_COLLECTION_NAME", "properties")
#
#     # MLflow
#     MLFLOW_TRACKING_URI: str = os.getenv("MLFLOW_TRACKING_URI", "")
#     MLFLOW_EXPERIMENT_NAME: str = os.getenv("MLFLOW_EXPERIMENT_NAME", "")
#     MLFLOW_RUN_ID_MODEL: str = os.getenv("MLFLOW_RUN_ID_MODEL", "")
#     MLFLOW_RUN_ID_METRIC: str = os.getenv("MLFLOW_RUN_ID_METRIC", "")
#     MLFLOW_MODEL_NAME: str = os.getenv("MLFLOW_MODEL_NAME", "")
#
#     # API / UI
#     API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")
#
#     # Reference mappings
#     CITY_MAPPING_PATH: str = os.getenv(
#         "CITY_MAPPING_PATH", "reference/city_mapping.json"
#     )
#     DISTRICT_MAPPING_PATH: str = os.getenv(
#         "DISTRICT_MAPPING_PATH", "reference/district_mapping.json"
#     )
#     DISTRICTS_BY_CITY_PATH: str = os.getenv(
#         "DISTRICTS_BY_CITY_PATH", "reference/districts_by_city.json"
#     )
#
#     # Datasets
#     RAW_DATA_PATH: str = os.getenv(
#         "RAW_DATA_PATH", "ml/dataset/raw/jakarta_properties_raw.csv"
#     )
#     PROCESSED_DATA_PATH: str = os.getenv(
#         "PROCESSED_DATA_PATH",
#         "ml/dataset/processed/jakarta_properties_processed.csv",
#     )
#
#     # Model artifacts
#     MODEL_PATH: str = os.getenv(
#         "MODEL_PATH", "artifacts/models/pipeline_model.pkl"
#     )
#     METRICS_PATH: str = os.getenv(
#         "METRICS_PATH", "artifacts/metrics/metrics.json"
#     )
#
#     # Logs
#     UNKNOWN_DISTRICT_LOG_PATH: str = os.getenv(
#         "UNKNOWN_DISTRICT_LOG_PATH", "log/unknown_district.log"
#     )
#
#
# settings = Settings()
