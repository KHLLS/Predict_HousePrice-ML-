import mlflow
from mlflow.tracking import MlflowClient
from config.settings import settings

class MLflowLoader:

    def __init__(self):
        mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)

        self.client = MlflowClient()

        self.run_id = settings.MLFLOW_RUN_ID_MODEL
        self.metric_run_id = settings.MLFLOW_RUN_ID_METRIC

        self.model_name = settings.MLFLOW_MODEL_NAME

    def load_model(self,version : str = "latest"):
        return mlflow.sklearn.load_model(
            f"models:/{self.model_name}/{version}"
        )

    def get_metrics(self):
        run = self.client.get_run(self.metric_run_id)
        return run.data.metrics

loader = MLflowLoader()

if __name__ == "__main__":
    load_pipeline = loader.load_model()
    load_metrics = loader.get_metrics()
    print(load_pipeline.steps)
    print(load_metrics)