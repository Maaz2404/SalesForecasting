import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_path:str = os.path.join("artifact","train.csv")
    test_path:str = os.path.join("artifact","test.csv")
    raw_data_path:str = os.path.join("artifact","raw.csv")
    
    

class DataIngestion:
    def __init__(self):
        self.config = DataIngestionConfig()
        
    def __merge_data(self, calendar, sales, sell_prices):
        logging.info("Merging data")
        try:
            sales_long = sales.melt(
                id_vars=["id", "item_id", "dept_id", "cat_id", "store_id", "state_id"],
                var_name="d",
                value_name="sales"
            )
            test = sales_long.copy()
            test = pd.merge(test, 
                calendar[['d', 'date', 'event_name_1','wm_yr_wk', 'snap_CA', 'snap_TX', 'snap_WI']], 
                on='d', 
                how='left')
            test["snap"] = test.apply(lambda row: row["snap_" + row["state_id"]], axis=1)
            test.drop(columns=['snap_CA', 'snap_TX', 'snap_WI'
                            ], inplace=True)
            data = pd.merge(test,sell_prices, on=['store_id', 'item_id', 'wm_yr_wk'], how='left')
            data['sell_price'] = data.groupby(['store_id', 'item_id'])['sell_price'].ffill()
            data['sell_price'] = data.groupby(['store_id', 'item_id'])['sell_price'].bfill()
            data.drop(columns=[ 'id', 'wm_yr_wk','d'], inplace=True)
            
            logging.info("Data merged successfully")
            
            return data.copy()
            
        except Exception as e:
            logging.error(f"Error in merging data: {e}")
            raise CustomException(e,sys)
        
        
    def read_data(self):
        logging.info("Reading data")
        try:
           calendar_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'calendar.csv')
           sales_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sales_train_validation.csv')
           prices_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sell_prices.csv') 
           calendar = pd.read_csv(calendar_file_path) 
           sales = pd.read_csv(sales_file_path,nrows=1000) 
           sell_prices = pd.read_csv(prices_file_path)
           logging.info("Data read successfully")
           data = self.__merge_data(calendar, sales, sell_prices)
           os.makedirs(os.path.dirname(self.config.train_path), exist_ok=True)
           
           data.to_csv(self.config.raw_data_path,header=True,index=False)
           
           logging.info("Train test split initiated")
           data['date'] = pd.to_datetime(data['date'])
           unique_dates = data['date'].sort_values().unique()
           split_date = unique_dates[int(len(unique_dates) * 0.8)]
           
           train = data[data['date'] < split_date]
           test = data[data['date'] >= split_date]
           
           train.to_csv(self.config.train_path,header=True,index=False)
           test.to_csv(self.config.test_path,header=True,index=False)
           
           return (
                self.config.train_path,
                self.config.test_path,
                
           )
           
           
        except Exception as e:
            logging.error(f"Error in reading data: {e}")
            raise CustomException(e,sys)      
        
if __name__ == "__main__":
    obj = DataIngestion()
    obj.read_data()        