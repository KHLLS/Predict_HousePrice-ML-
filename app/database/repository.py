from app.database.config import get_collection


class PropertyRepository:
    def __init__(self, collection=None):
        self.collection = collection or get_collection()

    def get_all(self):
        return list(self.collection.find({}, {"_id": 0}))
