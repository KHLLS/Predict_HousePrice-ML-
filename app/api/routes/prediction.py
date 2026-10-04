from fastapi import APIRouter, HTTPException
from app.api.schemas.prediction import PredictRequest, PredictResponse
from app.core.inference import predictor

router = APIRouter()

@router.post("/predict", response_model=PredictResponse)
def predict_price(body: PredictRequest):
    try:
        result = predictor.predict(body.model_dump())
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
