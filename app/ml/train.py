import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, median_absolute_error, mean_absolute_percentage_error
from sklearn.preprocessing import TargetEncoder
from xgboost import XGBRegressor
from app.ml.preprocessing import pipeline
import joblib, json


# LOAD DATA
df = pipeline()

# split X Y
X = df.drop(columns=['price_idr'])
y = df['price_idr']

te_district = TargetEncoder(
    smooth=1,
    cv=5,
    target_type='continuous'
)

te_subdistrict = TargetEncoder(
    smooth=1,
    cv=5,
    target_type='continuous'
)

te_district.fit(
    X[["district"]],
    y
)

te_subdistrict.fit(
    X[["sub_district"]],
    y
)

X["district"] = te_district.transform(
    X[["district"]]
)

X["sub_district"] = te_subdistrict.transform(
    X[["sub_district"]]
)

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

print("Train Model...")
model.fit(X, y)


# SAVE
joblib.dump(model, 'artifacts/models/model.pkl')
joblib.dump(te_district, 'artifacts/models/encoder/encoder_district.pkl')
joblib.dump(te_subdistrict, 'artifacts/models/encoder/encoder_subdistrict.pkl')


print("Saved model")

