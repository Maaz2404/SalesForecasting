from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import os
from src.pipelines.predict_pipeline import PredictPipeline
from typing import List
from datetime import timedelta
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

class IncomingData(BaseModel):
    sell_price:float
    store_id:str
    days_to_forecast:int
    
def forecast_sales(incoming: dict) -> List[float]:
    import pandas as pd
    from datetime import timedelta
    import os
    from src.pipelines.predict_pipeline import PredictPipeline

    df = pd.read_csv(os.path.join("artifact", "X_test.csv"))
    sales = pd.read_csv(os.path.join("artifact", "y_test.csv"))
    model = PredictPipeline()

    last_date = pd.to_datetime('2013-01-27')
    initial_days_since_start = df['days_since_start'].iloc[0]

    store_col = f"store_id_{incoming['store_id']}"
    if store_col not in df.columns:
        raise ValueError(f"Invalid store_id: {incoming['store_id']}")

    historical_sales = df[df[store_col] == 1].copy()
    sales = sales.loc[historical_sales.index].squeeze()
    past_sales = list(sales[-14:].values)

    forecast_dates = pd.date_range(start=last_date + timedelta(days=1), periods=incoming['days_to_forecast'])
    predicted_sales = []

    for i, date in enumerate(forecast_dates):
        row = {
            "sell_price": incoming['sell_price'],
            "snap": 0,
            "is_event": 0,
            "dayofweek": date.dayofweek,
            "day": date.day,
            "month": date.month,
            "is_weekend": int(date.dayofweek >= 5),
            "days_since_start": initial_days_since_start + i + 1,
            "lag_1": past_sales[-1],
            "lag_7": past_sales[-7],
            "lag_14": past_sales[-14],
            "store_id_CA_2": int(incoming['store_id'] == "CA_2"),
            "store_id_CA_3": int(incoming['store_id'] == "CA_3"),
            "store_id_CA_4": int(incoming['store_id'] == "CA_4"),
            "store_id_TX_1": int(incoming['store_id'] == "TX_1"),
            "store_id_TX_2": int(incoming['store_id'] == "TX_2"),
            "store_id_TX_3": int(incoming['store_id'] == "TX_3"),
            "store_id_WI_1": int(incoming['store_id'] == "WI_1"),
            "store_id_WI_2": int(incoming['store_id'] == "WI_2"),
            "store_id_WI_3": int(incoming['store_id'] == "WI_3"),
        }

        model_cols = [
            'sell_price', 'snap', 'is_event', 'dayofweek', 'day', 'month', 'is_weekend', 'days_since_start',
            'lag_1', 'lag_7', 'lag_14',
            'store_id_CA_2', 'store_id_CA_3', 'store_id_CA_4',
            'store_id_TX_1', 'store_id_TX_2', 'store_id_TX_3',
            'store_id_WI_1', 'store_id_WI_2', 'store_id_WI_3'
        ]
        row_df = pd.DataFrame([row])[model_cols]

        pred = float(model.predict(row_df)[0])  # ensure it's JSON serializable
        predicted_sales.append(pred)

        past_sales.append(pred)
        if len(past_sales) > 14:
            past_sales = past_sales[-14:]

    return predicted_sales


@app.get("/")
def home():
    return {"message": "Sales Forecasting App"}

@app.post("/predict")
def predict(data: IncomingData):
    try:
        preds = forecast_sales(data.dict())

        print("Preds:", preds)
        return {"predictions": preds}
    except Exception as e:
        print("Error during prediction:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})
        
    

