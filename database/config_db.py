from config.base import BaseConfig

class DBConfig(BaseConfig):
    # MongoDB — shared
    MONGO_URI : str
    MONGO_DB_NAME :str
    MONGO_COLLECTION_NAME :str

settings = DBConfig()