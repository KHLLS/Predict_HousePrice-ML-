import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import TargetEncoder
from sklearn.metrics import (r2_score, mean_absolute_error, median_absolute_error,
mean_absolute_percentage_error, mean_squared_error)
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from train.training.preprocessing import pipeline
from sklearn.pipeline import Pipeline
from config.base import settings
import mlflow
from mlflow.sklearn import SERIALIZATION_FORMAT_CLOUDPICKLE


class Train:
    def __init__(self):
        # LOAD DATA
        df = pipeline()

        # split dataset
        self.X = df.drop(columns=['price_idr'])
        self.y = df['price_idr']
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X,
            self.y,
            test_size=0.2,
            random_state=42
        )

        print("Split Dataset...")

        # MODEL
        self.model = XGBRegressor(
            objective='reg:absoluteerror',
            max_depth=10,
            learning_rate=0.05953139963770414,
            n_estimators=2747,
            subsample=0.8337433250519926,
            colsample_bytree=0.7543943678414979,
            reg_alpha=1.716855990003528, #L1 (menimalisasi fitur yang tidak penting agar tidak overfitting)
            reg_lambda=6.819289477686187, #L2 (menimalisasi nilai koefisien yang besar agar tidak overfitting)
            min_child_weight=6,
            gamma=0.032771478039126015,
            random_state=42,
            n_jobs=-1
        )


    def get_encoder(self,x):
        cat_cols = x.select_dtypes(exclude=np.number).columns
        num_cols = x.select_dtypes(include=np.number).columns
        return ColumnTransformer([
            ("target_encoder",TargetEncoder(smooth=1,cv=5,target_type="continuous"),cat_cols),
            ("numerical", "passthrough", num_cols),
        ],verbose_feature_names_out=False)

    def save_model(self,experiment_name,run_name,model_name,pipeline_model,metrics = None,mode = "evaluate"):
        # Set MLflow
        mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
        mlflow.set_experiment(experiment_name)

        # SAVE to MLflow
        with mlflow.start_run(run_name=run_name):
            mlflow.log_params(self.model.get_params())
            mlflow.sklearn.log_model(
                sk_model=pipeline_model,
                name=model_name,
                serialization_format=SERIALIZATION_FORMAT_CLOUDPICKLE,
            )
            if mode == "evaluate":
                mlflow.log_metrics(metrics)
        print("Saved model")

    def train_final(self):
        encoder = self.get_encoder(x=self.X)
        pipeline_final = Pipeline([
                ("encoder",encoder),
                ("model",self.model)
                ])

        print("Train Final Model")

        pipeline_final.fit(self.X, self.y)
        self.save_model(
            experiment_name="Housing Price Jakarta - Final Training",
            run_name="XGBoost - Final Model",
            model_name=settings.MLFLOW_MODEL_NAME,
            pipeline_model=pipeline_final,
            mode="final"
                        )

    def train_evaluate(self):
        encoder = self.get_encoder(x=self.X_train)
        pipeline_evaluate = Pipeline([
            ("encoder", encoder),
            ("model", self.model)
        ])
        print("Train Evaluate Model")
        pipeline_evaluate.fit(self.X_train, self.y_train)
        y_pred = pipeline_evaluate.predict(self.X_test)
        y_test_true = np.expm1(self.y_test)
        y_pred_true = np.expm1(y_pred)
        error_pct = (np.abs(y_pred_true - y_test_true) / y_test_true)
        mlflow.set_experiment("Housing Price Jakarta - Evaluate")

        result = {
            "R2_Score": r2_score(self.y_test, y_pred),
            "MAE": mean_absolute_error(y_test_true, y_pred_true),
            "MDAE": median_absolute_error(y_test_true, y_pred_true),
            "MAPE": mean_absolute_percentage_error(y_test_true, y_pred_true),
            "MSE":mean_squared_error(y_test_true,y_pred_true),
            "Q25": error_pct.quantile(0.25),
            "Q50": error_pct.quantile(0.50),
            "Q75": error_pct.quantile(0.75)
        }

        self.save_model(
            experiment_name="Housing Price Jakarta - Evaluate",
            run_name="XGBoost - Evaluate Model",
            model_name=settings.MLFLOW_MODEL_NAME,
            pipeline_model=pipeline_evaluate,
            metrics=result
                        )

if __name__ == "__main__":
    train = Train()
    train_final = train.train_final()
    train_evaluate = train.train_evaluate()




