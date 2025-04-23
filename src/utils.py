import dill
import pickle
from sklearn.metrics import r2_score,mean_squared_error
from src.logger import logging
from src.exception import CustomException
import numpy as np
import sys
import os

def load_object(file_path):
    """
    Load a Python object from a pickle file.

    Args:
        file_path (str): Path to the pickle file.

    Returns:
        object: The loaded Python object.
    """
    try:
        with open(file_path, 'rb') as file:
            obj = dill.load(file)
        return obj
    except Exception as e:
        print(f"Error loading object from {file_path}: {e}")
        return None

def save_object(file_path, obj):
    """
    Save a Python object to a pickle file.

    Args:
        file_path (str): Path to the pickle file.
        obj (object): The Python object to save.

    Returns:
        None
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)        
        with open(file_path, 'wb') as file:
            dill.dump(obj, file)
    except Exception as e:
        print(f"Error saving object to {file_path}: {e}")
    
def evaluate_models(x_train, y_train, x_test, y_test, models):
    """
    Evaluate multiple regression models and return the best one based on R2 score.

    Args:
        x_train (pd.DataFrame): Training features.
        y_train (pd.Series): Training target variable.
        x_test (pd.DataFrame): Testing features.
        y_test (pd.Series): Testing target variable.
        models (dict): Dictionary of model names and their corresponding instances.

    Returns:
        dict: Dictionary containing model names and their R2 scores.
    """
    model_report = {}
    
    for model_name, model in models.items():
        try:
            logging.info(f"Training {model_name}")
            model.fit(x_train, y_train)
            logging.info(f"Evaluating {model_name}")
            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)
            
            train_mse = mean_squared_error(y_train, y_train_pred)
            test_mse = mean_squared_error(y_test, y_test_pred)
            train_rmse = np.sqrt(train_mse)
            test_rmse = np.sqrt(test_mse)
            
            train_r2 = r2_score(y_train, y_train_pred)
            test_r2 = r2_score(y_test, y_test_pred)
            
            logging.info(f"{model_name} - Train RMSE: {train_rmse}, Test RMSE: {test_rmse}")
            logging.info(f"{model_name} - Train R2: {train_r2}, Test R2: {test_r2}")
            
            # Use test R2 as the evaluation metric
            r2 = test_r2
            
            model_report[model_name] = r2
        except Exception as e:
            logging.error(f"Error evaluating {model_name}: {e}")
            raise CustomException(e, sys)
        
    
    return model_report