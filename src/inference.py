import numpy as np
import pandas as pd
import joblib, json

def load_models():
    model   = joblib.load("models/model.pkl")
    encoder = joblib.load("models/encoder/encoder.pkl")
    with open("models/metrics_model.json", "r") as file:
        metrics = json.load(file)
    return model, encoder, metrics

def predict(data):
    model, encoder, metrics = load_models()

    df = pd.DataFrame([data])

    # Log transform (sama dengan training)
    df['land_size_m2']     = np.log1p(df['land_size_m2'])
    df['building_size_m2'] = np.log1p(df['building_size_m2'])

    # OHE city
    city_cols = [
        'city_Jakarta Barat',
        'city_Jakarta Pusat',
        'city_Jakarta Selatan',
        'city_Jakarta Timur',
        'city_Jakarta Utara',
    ]
    for col in city_cols:
        df[col] = 0
    city_key = f"city_{data.get('city', '')}"
    if city_key in city_cols:
        df[city_key] = 1
    df = df.drop(columns=['city'], errors='ignore')

    # Encode district
    df['district'] = encoder.transform(df[['district']]).flatten()

    # Prediksi
    df = df[model.feature_names_in_]
    price_log = model.predict(df)[0]
    price = np.expm1(price_log)

    # Membuat range prediksi dari harga low sampai high menggunakan median presentase error
    return {
        "price": round(price),
        "price_low": round(price - (price * metrics['Q50'])),
        "price_high": round(price + (price * metrics['Q50'])),
    }

