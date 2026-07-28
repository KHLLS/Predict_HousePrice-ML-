from fastapi import FastAPI
from app.api.routes.routes_predict import router as predict_router

app = FastAPI(
    title="Jakarta Property Price Predictor",
    description="API prediksi harga properti Jakarta menggunakan XGBoost ensemble.",
    version="1.0.0",
)
app.include_router(predict_router, prefix="/api/v1", tags=["Prediksi Harga"])
