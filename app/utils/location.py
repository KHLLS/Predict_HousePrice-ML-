from app.inference import predictor
import json

def load_city():
    if predictor.pipeline is None:
        return ["Jakarta Pusat", "Jakarta Selatan", "Jakarta Timur", "Jakarta Barat", "Jakarta Utara"]
    feature = list(predictor.pipeline.feature_names_in_)
    city_map = [c.removeprefix("city_") for c in feature if c.startswith("city_")]
    with open("data/city_mapping.json","w") as f:
        city_mapping = json.dump(city_map,f,indent=4)
    return city_mapping

def load_districts():
    pass

load_city()