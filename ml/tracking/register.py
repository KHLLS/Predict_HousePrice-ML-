import mlflow
from config.base import settings

class MLflowRegister():
    def __init__(self):
        self.model_name = settings.MLFLOW_MODEL_NAME
        self.run_id = settings.MLFLOW_RUN_ID_MODEL

    def register(self):
        return mlflow.register_model(
            f"runs:/{self.run_id}/{self.model_name}",self.model_name
        )

register = MLflowRegister()
register.register()