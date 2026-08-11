from config.base import BaseConfig


class MLConfig(BaseConfig):
    # Tambahan khusus ML
    MLFLOW_TRACKING_URI : str
    MLFLOW_MODEL_NAME : str
    MLFLOW_RUN_ID_MODEL : str
    MLFLOW_RUN_ID_METRIC : str

settings = MLConfig()