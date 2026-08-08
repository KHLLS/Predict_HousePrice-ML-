from app.inference import predictor

class PredictionService:
    def predict(self, payload: dict):
        return predictor.predict(payload)
