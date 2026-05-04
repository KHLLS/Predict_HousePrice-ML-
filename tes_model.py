import pandas as pd
import numpy as np
import joblib

def load_data():
    model_main = joblib.load('models/model_main.pkl')
    model_elite = joblib.load('models/model_elite.pkl')
    encoder_main = joblib.load('models/encoder/encoder_main.pkl')
    encoder_elite = joblib.load('models/encoder/encoder_elite.pkl')
    return model_main, model_elite,encoder_main, encoder_elite

model_main, model_elite,encoder_main, encoder_elite = load_data()

# print(model.feature_names_in_)
def format_rupiah(x):
    return f"Rp {int(x):,}".replace(",", ".")

col = {
    'bedrooms': 5,
    'bathrooms': 5,
    'garage' : 2,
    'land_size_m2': np.log1p(433),
    'building_size_m2' : np.log1p(350),
    'cluster': 0,
    'pool' : 0,
    'mrt' : 0,
    'tol' : 0,
    'mall' : 0,
    'scbd' : 0,
    'city_Jakarta Barat': 0,
    'city_Jakarta Pusat': 0,
    'city_Jakarta Selatan': 1,
    'city_Jakarta Timur': 0,
    'city_Jakarta Utara': 0,
}

df = pd.DataFrame([col])
df['district'] = 'Pondok Indah'
df['district_encoded'] = encoder_main.transform(df[['district']]).flatten()
df = df.drop(columns='district')
df = df[model_main.feature_names_in_]
predict = model_main.predict(df)[0]
# predict = np.expm1(predict)
print(format_rupiah(predict))

if predict > 20_000_000_000:
    df_elite = pd.DataFrame([col])
    df_elite['district'] = 'Senopati'
    df_elite['district_encoded'] = encoder_elite.transform(df_elite[['district']]).flatten()
    df_elite = df_elite.drop(columns='district')
    predict = model_elite.predict(df_elite)[0]
    # predict = np.expm1(predict)
    print(format_rupiah(predict))

