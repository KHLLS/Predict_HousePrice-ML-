from fastapi import APIRouter, HTTPException
from api.schemas.schemas_predict import PredictRequest, PredictResponse
from src.inference import predictor

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
