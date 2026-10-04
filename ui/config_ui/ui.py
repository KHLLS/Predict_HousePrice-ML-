from config.base import BaseConfig

class UIConfig(BaseConfig):
    API_URL: str
    UI_TITLE: str = "Prediksi Harga Rumah Jakarta"

settings = UIConfig()