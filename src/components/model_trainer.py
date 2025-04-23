from dataclasses import dataclass
import os
import sys
from src.logger import logging
from src.exception import CustomException
from src.utils import save_object, load_object
from sklearn.tree import DecisionTreeRegressor
import pandas as pd
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
from src.utils import evaluate_models

@dataclass
class ModelTrainerConfig:
    model_path: str = os.path.join("artifact", "model.pkl")
    
class ModelTrainer:
    def __init__(self):
        self.model_config = ModelTrainerConfig()
        
    def initiate_modelling(self):
        try:
            logging.info("Starting loading data")
            X_train = pd.read_csv(os.path.join("artifact", "X_train.csv"))
            y_train = pd.read_csv(os.path.join("artifact", "y_train.csv"))
            X_test = pd.read_csv(os.path.join("artifact", "X_test.csv"))
            y_test = pd.read_csv(os.path.join("artifact", "y_test.csv"))
            logging.info("Data loaded successfully")
            
            
            models = {
                    "Random Forest"  : RandomForestRegressor(),
                    "Decision Tree"  : DecisionTreeRegressor(),
                    "XGBoost"        : XGBRegressor(),
                    "Linear Regression": LinearRegression()
                } 
            model_report:dict = evaluate_models(X_train, y_train, X_test, y_test, models)  
            
            best_score = max(sorted(model_report.values())) 
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_score)]
            best_model = models[best_model_name]
            
            logging.info(f"Best model found: {best_model_name} with score: {best_score}")
            
            save_object(self.model_config.model_path,best_model)
            
            
        except Exception as e:
            logging.error(f"Error in model training: {e}")
            raise CustomException(e, sys)            


if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.initiate_modelling()