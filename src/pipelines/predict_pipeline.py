import sys
import pandas as pd
import numpy as np
import pickle
from src.exception import CustomException
from src.utils import load_object
import os

class PredictPipeline:
    def __init__(self):
        self.model_path = os.path.join("artifact", "model.pkl")
        self.model = load_object(file_path=self.model_path)
        
    def predict(self, features: pd.DataFrame):
        try:
            preds = self.model.predict(features)
            return preds
        except Exception as e:
            raise CustomException(e,sys)
        
class CustomData:
    def __init__(
        self,
        sell_price: float,
        snap: int,
        is_event: int,
        dayofweek: int,
        day: int,
        month: int,
        is_weekend: int,
        days_since_start: int,
        lag_1: float,
        lag_7: float,
        lag_14: float,
        store_id_CA_2: int,
        store_id_CA_3: int,
        store_id_CA_4: int,
        store_id_TX_1: int,
        store_id_TX_2: int,
        store_id_TX_3: int,
        store_id_WI_1: int,
        store_id_WI_2: int,
        store_id_WI_3: int,
    ):
        self.sell_price = sell_price
        self.snap = snap
        self.is_event = is_event
        self.dayofweek = dayofweek
        self.day = day
        self.month = month
        self.is_weekend = is_weekend
        self.days_since_start = days_since_start
        self.lag_1 = lag_1
        self.lag_7 = lag_7
        self.lag_14 = lag_14
        self.store_id_CA_2 = store_id_CA_2
        self.store_id_CA_3 = store_id_CA_3
        self.store_id_CA_4 = store_id_CA_4
        self.store_id_TX_1 = store_id_TX_1
        self.store_id_TX_2 = store_id_TX_2
        self.store_id_TX_3 = store_id_TX_3
        self.store_id_WI_1 = store_id_WI_1
        self.store_id_WI_2 = store_id_WI_2
        self.store_id_WI_3 = store_id_WI_3
 
    def get_data_as_dataframe(self):
        try:
            data_dict = {
                "sell_price": [self.sell_price],
                "snap": [self.snap],
                "is_event": [self.is_event],
                "dayofweek": [self.dayofweek],
                "day": [self.day],
                "month": [self.month],
                "is_weekend": [self.is_weekend],
                "days_since_start": [self.days_since_start],
                "lag_1": [self.lag_1],
                "lag_7": [self.lag_7],
                "lag_14": [self.lag_14],
                "store_id_CA_2": [self.store_id_CA_2],
                "store_id_CA_3": [self.store_id_CA_3],
                "store_id_CA_4": [self.store_id_CA_4],
                "store_id_TX_1": [self.store_id_TX_1],
                "store_id_TX_2": [self.store_id_TX_2],
                "store_id_TX_3": [self.store_id_TX_3],
                "store_id_WI_1": [self.store_id_WI_1],
                "store_id_WI_2": [self.store_id_WI_2],
                "store_id_WI_3": [self.store_id_WI_3],
            }
            df = pd.DataFrame(data_dict)
            return df
        except Exception as e:
            raise CustomException(e, sys)