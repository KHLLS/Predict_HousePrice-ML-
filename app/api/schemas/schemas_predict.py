from pydantic import BaseModel, Field
from typing import Literal, ClassVar, List
from app.ml.inference import predictor


def load_city():
    feature = list(predictor.model.feature_names_in_)
    city_map = [c.removeprefix("city_") for c in feature if c.startswith("city_")]
    return city_map


class PredictRequest(BaseModel):
    city_map: ClassVar[List] = load_city()
    district: str
    sub_district: str
    city: str
    bedrooms: int = Field(gt=0)
    bathrooms: int = Field(gt=0)
    garage: int = Field(ge=0)
    land_size_m2: float = Field(gt=30)
    building_size_m2: float = Field(gt=30)
    cluster: int = Field(0, ge=0, le=1)
    pool: int = Field(0, ge=0, le=1)
    mrt: int = Field(0, ge=0, le=1)
    tol: int = Field(0, ge=0, le=1)
    mall: int = Field(0, ge=0, le=1)


class PredictResponse(BaseModel):
    price: float
    price_low: float
    price_high: float
