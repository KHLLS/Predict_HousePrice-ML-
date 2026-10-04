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
    MODEL_PATH: Path = BASE_DIR / "artifacts" / "models" / "pipeline_model.pkl"
    METRICS_PATH: Path = BASE_DIR / "artifacts" / "metrics" / "metrics.json"

    model_config = ConfigDict(
        extra="ignore",
        env_file=str(BASE_DIR / ".env")
    )

settings = BaseConfig()
