from fastapi import APIRouter, HTTPException
from app.api.schemas.schemas_predict import PredictRequest, PredictResponse
from app.services.prediction_service import PredictionService

router = APIRouter()
service = PredictionService()


@router.post("/predict", response_model=PredictResponse)
def predict_price(body: PredictRequest):
    try:
        result = service.predict(body.model_dump())
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
