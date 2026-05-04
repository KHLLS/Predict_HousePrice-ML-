import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, median_absolute_error
from sklearn.preprocessing import TargetEncoder
from xgboost import XGBRegressor
from prepocessing import pipeline
import joblib


# LOAD DATA
df = pipeline()

# split dataset
df_main = df.copy()
df_elite = df[df['price_idr'] >= 15_000_000_000].copy()

print(f"Elite Presentage: {(len(df_elite) / len(df_main)) * 100}")


# FUNCTION TRAIN
def train_model(df, name):
    print(f"\n=== TRAINING {name.upper()} MODEL ===")

    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

    # split X Y
    X_train = train_df.drop(['price_idr'], axis=1).copy()
    y_train = train_df['price_idr']

    X_test = test_df.drop(['price_idr'], axis=1).copy()
    y_test = test_df['price_idr']

    # ENCODER (FIT ONLY ON TRAIN)
    te = TargetEncoder(smooth=10, cv=5, target_type='continuous')

    X_train['district_encoded'] = te.fit_transform(
        X_train[['district']], y_train
    ).flatten()

    X_test['district_encoded'] = te.transform(
        X_test[['district']]
    ).flatten()

    # drop original
    X_train.drop(columns='district', inplace=True)
    X_test.drop(columns='district', inplace=True)

    # MODEL
    model = XGBRegressor(
        objective='reg:absoluteerror',
        max_depth=7,
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

    print(f"Train R2: {r2_score(y_train, train_pred)}")
    print(f"Test R2 : {r2_score(y_test, test_pred)}")
    print(f"MAE :  {mean_absolute_error(y_test, test_pred)}")
    print(f"MDAE: {median_absolute_error(y_test, test_pred)}")

    # SAVE
    joblib.dump(model, f'models/model_{name}.pkl')
    joblib.dump(te, f'models/encoder/encoder_{name}.pkl')

    print(f"Saved: {name}")

    # FEATURE IMPORTANCE
    feat_imp = pd.DataFrame({
        'feature': X_train.columns,
        'importance': model.feature_importances_
    }).sort_values(by='importance', ascending=False)

    print(feat_imp.head(10))

    return model, te


# TRAIN BOTH
model_main, encoder_main = train_model(df_main, "main")
model_elite, encoder_elite = train_model(df_elite, "elite")