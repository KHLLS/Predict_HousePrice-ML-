import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, median_absolute_error, mean_absolute_percentage_error
from sklearn.preprocessing import TargetEncoder
from xgboost import XGBRegressor
from src.ml.preprocessing import pipeline
import joblib, json


# LOAD DATA
df = pipeline()

# split X Y
X = df.drop(columns=['price_idr'])
y = df['price_idr']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

te_district = TargetEncoder(
    smooth=10,
    cv=5,
    target_type='continuous'
)

te_subdistrict = TargetEncoder(
    smooth=10,
    cv=5,
    target_type='continuous'
)

X_train['district'] = te_district.fit_transform(
    X_train[['district']],
    y_train
).ravel()

X_test['district'] = te_district.transform(
    X_test[['district']]
).ravel()

X_train['sub_district'] = te_subdistrict.fit_transform(
    X_train[['sub_district']],
    y_train
).ravel()

X_test['sub_district'] = te_subdistrict.transform(
    X_test[['sub_district']]
).ravel()

# MODEL
model = XGBRegressor(
    objective='reg:absoluteerror',
    max_depth=8,
    learning_rate=0.03,
    n_estimators=900,
    subsample=0.8,
    colsample_bytree=0.7,
    reg_alpha=1,
    reg_lambda=2,
    min_child_weight=5,
    gamma=0.1,
    random_state=42
)

model.fit(X_train, y_train)

# EVALUATION
train_pred = model.predict(X_train)
test_pred = model.predict(X_test)
y_test_true = np.expm1(y_test)
y_pred_true = np.expm1(test_pred)

print(f"Train R2: {r2_score(y_test,test_pred)}")
print(f"Test R2 : {r2_score(y_test_true,y_pred_true)}")
print(f"MAE :  {mean_absolute_error(y_test_true,y_pred_true)}")
print(f"MDAE: {median_absolute_error(y_test_true,y_pred_true)}")
print(f"MAPE: {mean_absolute_percentage_error(y_test_true,y_pred_true)}")

# SAVE
joblib.dump(model, 'models/model.pkl')
joblib.dump(te_district, 'models/encoder/encoder_district.pkl')
joblib.dump(te_subdistrict, 'models/encoder/encoder_subdistrict.pkl')

error_pct = (np.abs(y_pred_true - y_test_true) / y_test_true)
metrics = {
        "Model" : "XGBRegressor",
        "R2 Score":r2_score(y_test_true,y_pred_true),
        "MAE (mean)":mean_absolute_error(y_test_true,y_pred_true),
        "MDAE (median)": median_absolute_error(y_test_true,y_pred_true),
        "MAPE": mean_absolute_percentage_error(y_test_true,y_pred_true),
        "Q25": error_pct.quantile(0.25),
        "Q50": error_pct.quantile(0.50),
        "Q75": error_pct.quantile(0.75),
    }

with open('models/metrics_model.json', 'w') as f:
    json.dump(metrics, f, ensure_ascii=False, indent=4)

print("Saved model")

# FEATURE IMPORTANCE
feat_imp = pd.DataFrame({
    'feature': X_train.columns,
    'importance': model.feature_importances_
}).sort_values(by='importance', ascending=False)

print(feat_imp.head(10))