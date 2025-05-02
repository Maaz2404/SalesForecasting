from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import pickle
from src.pipelines.predict_pipeline import CustomData,PredictPipeline


app = FastAPI()
class InputData(BaseModel):
    sell_price: float
    snap: int
    is_event: int
    dayofweek: int
    day: int
    month: int
    is_weekend: int
    days_since_start: int
    lag_1: float
    lag_7: float
    lag_14: float
    store_id_CA_2: int
    store_id_CA_3: int
    store_id_CA_4: int
    store_id_TX_1: int
    store_id_TX_2: int
    store_id_TX_3: int
    store_id_WI_1: int
    store_id_WI_2: int
    store_id_WI_3: int


@app.get("/")
def home():
    return {"message": "Sales Forecasting App"}

@app.post("/predict")
def predict(data: InputData):
    try:
        # Convert incoming data into CustomData object
        custom_data = CustomData(
            sell_price = data.sell_price,
            snap = data.snap,
            is_event = data.is_event,
            dayofweek = data.dayofweek,
            day = data.day,
            month = data.month,
            is_weekend = data.is_weekend,
            days_since_start = data.days_since_start,
            lag_1 = data.lag_1,
            lag_7 = data.lag_7,
            lag_14 = data.lag_14,
            store_id_CA_2 = data.store_id_CA_2,
            store_id_CA_3 = data.store_id_CA_3,
            store_id_CA_4 = data.store_id_CA_4,
            store_id_TX_1 = data.store_id_TX_1,
            store_id_TX_2 = data.store_id_TX_2,
            store_id_TX_3 = data.store_id_TX_3,
            store_id_WI_1 = data.store_id_WI_1,
            store_id_WI_2 = data.store_id_WI_2,
            store_id_WI_3 = data.store_id_WI_3,
        )

        # Prepare dataframe
        final_input_df = custom_data.get_data_as_dataframe()

        # Predict
        pipeline = PredictPipeline()
        prediction = pipeline.predict(final_input_df)

        return {"prediction": prediction.tolist()}
    
    except Exception as e:
        return {"error": str(e)}


