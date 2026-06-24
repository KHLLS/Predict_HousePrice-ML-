import pandas as pd
import numpy as np
import json
from pathlib import Path
from src.database.config import coll

MAPPING_PATH = "data/district_mapping.json" # mapping district -> kecamatan
LOG_UNKNOWN_PATH = "log/unknown_district.log" # log district yang belum ada di mapping

# Load dataset from database
def load_dataset():
    data = coll.find({},{"_id":0})
    df = pd.DataFrame(list(data))
    return df

# Standarization Collumns
def standard(df):
    df['price_idr'] = pd.to_numeric(df['price_idr'], errors='coerce')
    df['garage'] = df['garage'].fillna(0)
    df['title'] = df['title'].str.lower()
    return df

#  Filtering Collumns
def filtering(df):
    map_col = ['bedrooms','bathrooms','garage']
    for col in map_col:
        df = df[(df[col] != df['land_size_m2']) & (df[col] != df['building_size_m2'])]
    df = df[(df['price_idr'] > 0) & (df['bedrooms'] > 0) & (df['bathrooms'] > 0)]
    df = df[(df['building_size_m2'] >= 30) & (df['land_size_m2'] >= 30 )]
    df = df[(df['bedrooms'] <= 30) & (df['bathrooms'] <= 30) & (df['garage'] <= 30)]
    df = df.dropna(axis=0)
    df = df[(df['rumah_sakit'] == 0) & (df['kos'] == 0)]
    lower = df['price_idr'].quantile(0.1)
    upper = df['price_idr'].quantile(0.98)
    df = df[
        (df['price_idr'] >= lower) &
        (df['price_idr'] <= upper)
    ]
    return df

# Feature engineering
def feature(df):
    df['cluster'] = df['title'].str.contains(
        'cluster', na=False
        ).astype(int)
    df['pool'] = df['title'].str.contains(
        r'kolam renang|pool', na=False
        ).astype(int)
    df['mrt'] = df['title'].str.contains(
        r'mrt', na=False
        ).astype(int)
    df['tol'] = df['title'].str.contains(
        r'tol', na=False
        ).astype(int)
    df['mall'] = df['title'].str.contains(
        r'mall', na=False
        ).astype(int)
    df['kos'] = df['title'].str.contains(
        r'kos|kost|kostan|kosan', na=False
        ).astype(int)
    df['rumah_sakit'] = (df['title'].str.contains(
        r'rumah sakit', na=False) &~ df['title'].str.contains(r'dekat|near|sekitar|selangkah', na=False)
        ).astype(int)
    return df

# Transformization
def transform(df):
    df['land_size_m2'] = np.log1p(df['land_size_m2'])
    df['building_size_m2'] = np.log1p(df['building_size_m2'])
    df['price_idr'] = np.log1p(df['price_idr'])
    return df

# Encode
def encode(df):
    df = pd.get_dummies(df, columns=['city'], dtype=int) #One Hot Encoding (OHE)
    return df

# Drop collumns
def drop(df):
    df = df.drop(columns=['title','scraped_at','rumah_sakit','kos'])
    return df

# Mapping district ke kecamatan, log district yang belum ada di mapping
def district_mapping(df):
    with open(MAPPING_PATH, "r") as file:
        mapping = json.load(file)

    df['district'] = df['district'].str.lower()
    unknown = set(df[~df['district'].isin(mapping.keys())]['district'].unique())

    if len(unknown) > 0:
        print(f"{len(unknown)} district tidak ada di mapping:")
        for d in sorted(unknown):
            print(f" - '{d}'")

    log_unknown = Path(LOG_UNKNOWN_PATH)
    logged = set()
    if log_unknown.exists():
        with open(log_unknown, "r") as file:
            logged = {i.strip() for i in file}

    new_unknown = unknown - logged
    if new_unknown:
        with open(log_unknown, "a") as file:
            for d in sorted(new_unknown):
                file.write(f"{d}\n")

    df['district'] = df['district'].map(mapping)
    return df

# Run Pipeline
def pipeline():
    df = load_dataset()
    df = standard(df)
    df = feature(df)
    df = filtering(df)
    df = transform(df)
    df = encode(df)
    df = drop(df)
    df = district_mapping(df)
    return df

# Save
def save(df):
    df.to_csv('data/processed/jakarta_properties_processed_tes.csv',index=False)

# Save if run in this file
if __name__ == "__main__":
    df = pipeline()
    save(df)