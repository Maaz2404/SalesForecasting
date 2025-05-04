from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.logger import logging
from src.exception import CustomException
import sys
import os

class TrainingPipeline:
    def __init__(self, run_ingestion=True, run_transformation=True, run_training=True):
        self.run_ingestion = run_ingestion
        self.run_transformation = run_transformation
        self.run_training = run_training

        self.data_ingestion = DataIngestion()
        self.data_transformation = DataTransformation()
        self.model_trainer = ModelTrainer()

    def run_pipeline(self):
        try:
            logging.info("Pipeline started")

            if self.run_ingestion:
                self.data_ingestion.read_data()
                logging.info("Data ingestion completed")
            else:
                logging.info("Skipping data ingestion")

            if self.run_transformation:
                self.data_transformation.initiate_data_transformation()
                logging.info("Data transformation completed")
            else:
                logging.info("Skipping data transformation")
                

            if self.run_training:
                self.model_trainer.initiate_modelling(
                    
                )
                logging.info("Model training completed")
            else:
                logging.info("Skipping model training")

            logging.info("Pipeline completed successfully")

        except Exception as e:
            logging.error(f"Error in training pipeline: {e}")
            raise CustomException(e, sys)


if __name__ == "__main__":
    # Example usage: run only transformation and training
    pipeline = TrainingPipeline(run_ingestion=False, run_transformation=False, run_training=True)
    pipeline.run_pipeline()
