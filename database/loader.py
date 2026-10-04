import pandas as pd
from database.repository import PropertyRepository


class DatasetLoader:
    _cache = None

    @classmethod
    def load_dataset(cls, refresh=False):
        if cls._cache is not None and not refresh:
            return cls._cache.copy()

        repository = PropertyRepository()
        data = repository.get_all()
        df = pd.DataFrame(data)
        cls._cache = df
        return cls._cache.copy()
