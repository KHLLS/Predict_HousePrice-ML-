import pandas as pd
import numpy as np

PATH = "data/raw/jakarta_properties_baru.csv" # input path sample data

# Load dataset from path
def load_dataset(path):
    df = pd.read_csv(path)
    return df

# Standarization Collumns
def standard(df):
    df['price_idr'] = pd.to_numeric(df['price_idr'], errors='coerce')
    df['garage'] = df['garage'].fillna(0)
    df['title'] = df['title'].str.lower()
    df['district'] = df['district'].str.lower()
    return df

#  Filtering Collumns
def filtering(df):
    map_col = ['bedrooms','bathrooms','garage']
    for col in map_col:
        df = df[(df[col] != df['land_size_m2']) & (df[col] != df['building_size_m2'])]
    df = df[(df['price_idr'] > 0) & (df['bedrooms'] > 0) & (df['bathrooms'] > 0)]
    df = df[(df['building_size_m2'] >= 30) & (df['land_size_m2'] >= 30 )]
    # df['bedrooms']  = df['bedrooms'].clip(upper=20)
    # df['bathrooms'] = df['bathrooms'].clip(upper=20)
    # df['garage']    = df['garage'].clip(upper=20)
    df['price_idr'] = df['price_idr'].clip(
        df['price_idr'].quantile(0.02),
        df['price_idr'].quantile(0.98))
    df = df.drop(index=df[(df['price_idr'] > 100_000_000_000) & ((df['land_size_m2'] < 100) | (df['building_size_m2'] < 100))].index)

    df = df[(df['rumah_sakit'] == 0) & (df['kos'] == 0)]
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
    df['scbd'] = df['title'].str.contains(
        r'scbd', na=False
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
    # df['price_idr_log'] = np.log1p(df['price_idr'])
    return df

# Encode 
def encode(df):
    df = pd.get_dummies(df, columns=['city'], dtype=int) #One Hot Encoding (OHE)
    return df

# Drop collumns 
def drop(df):
    df = df.dropna(axis=0)
    df = df.drop(columns=['title','scraped_at','rumah_sakit','kos'])
    return df

# Run Pipeline
def pipeline():
    df = load_dataset(PATH)
    df = standard(df)
    df = feature(df)
    df = filtering(df)
    df = transform(df)
    df = encode(df)
    df = drop(df)
    return df

# Save
def save(df):
    df.to_csv('data/processed/jakarta_properties_clear.csv',index=False)

# Save if run in this file
if __name__ == "__main__":
    df = pipeline()
    save(df)



