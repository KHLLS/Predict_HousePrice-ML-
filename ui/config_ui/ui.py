from config.base import BaseConfig

class UIConfig(BaseConfig):
    API_URL: str = "http://localhost:8000"
    UI_TITLE: str = "Prediksi Harga Rumah Jakarta"

settings = UIConfig()