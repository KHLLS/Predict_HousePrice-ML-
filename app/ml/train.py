import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import TargetEncoder
from xgboost import XGBRegressor
from app.ml.preprocessing import pipeline
from sklearn.pipeline import Pipeline
import joblib


# LOAD DATA
df = pipeline()

# split X Y
X = df.drop(columns=['price_idr'])
y = df['price_idr']

print("Split Dataset...")

# MODEL
model = XGBRegressor(
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
    random_state=42
)

cat_cols = X.select_dtypes(exclude=np.number).columns
num_cols = X.select_dtypes(include=np.number).columns
encoder = ColumnTransformer([
    (
        "target_encoder",
        TargetEncoder(
            smooth=1,
            cv=5,
            target_type="continuous"
        ),
        cat_cols
    ),
    ("numerical", "passthrough", num_cols),
],verbose_feature_names_out=False)

pipeline = Pipeline([
        ("encoder",encoder),
        ("model",model)
        ])

print("Train Model...")

pipeline.fit(X, y)


# SAVE
joblib.dump(pipeline, "artifacts/models/model.pkl")

print("Saved model")

