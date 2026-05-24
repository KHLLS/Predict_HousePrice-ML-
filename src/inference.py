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

class Predict():
    num_col = ['bedrooms','bathrooms','garage','land_size_m2','building_size_m2']
    def __init__(self,data):
        self.data = data
    
    def validation(self):
        data = self.data
        for i in self.num_col:
            if i == 'garage':
                if data.loc[0,i] < 0:
                    raise ValueError('garage must be >= 0')
            elif data.loc[0,i] <= 0:
                raise ValueError(f'{i} must be > 0')
        return data
    
    def transformation(self):
        df = self.validation().copy()
        df['land_size_m2'] = np.log1p(df['land_size_m2'])
        df['building_size_m2'] = np.log1p(df['building_size_m2'])
        return df

    def predict(self):
        df = self.transformation()
        df_main = df.copy()
        df_main['district_encoded'] = encoder_main.transform(df_main[['district']]).flatten()
        df_main = df_main.drop(columns='district')
        df_main = df_main[model_main.feature_names_in_]
        result = model_main.predict(df_main)[0]
        if result >= 20_000_000_000:
            df_elite = df.copy()
            df_elite['district_encoded'] = encoder_elite.transform(df_elite[['district']]).flatten()
            df_elite = df_elite.drop(columns='district')
            df_elite = df_elite[model_elite.feature_names_in_]
            result = model_elite.predict(df_elite)[0]
        return result
    
if __name__ == '__main__':
    tes = Predict()





            
