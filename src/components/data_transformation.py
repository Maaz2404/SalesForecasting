from src.exception import CustomException
from src.logger import logging
import os
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

from dataclasses import dataclass
import sys


@dataclass
class DataTransformationConfig:
    train_path: str = os.path.join("artifact", "train.csv")
    test_path: str = os.path.join("artifact", "test.csv")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
        self.start_date = None  # <-- NEW: Store the earliest date for global days_since_start

    def _aggregate(self, df):
        try:
            logging.info("Starting data aggregation")
            df['date'] = df['date'].astype('datetime64[ns]')
            df.set_index('date', inplace=True)
            df.sort_index(inplace=True)
            agg = df.groupby([df.index, 'store_id']).agg({
                'sales': 'sum',
                'sell_price': 'mean',
                'snap': 'mean',
                'event_name_1': 'first'
            }).reset_index()  # Reset index to retain 'store_id' as a column
            agg['is_event'] = agg['event_name_1'].apply(lambda x: 0 if x == 'No Event' else 1)
            agg['is_event'] = agg['is_event'].astype('int')
            agg.drop(columns=['event_name_1'], inplace=True)
            agg['date'] = pd.to_datetime(agg['date'])  # Ensure 'date' is datetime
            agg.set_index('date', inplace=True)  # Set 'date' back as the index
            logging.info("Data aggregation completed")
            return agg
        except Exception as e:
            logging.error(f"Error in data aggregation: {e}")
            raise CustomException(e, sys)

    def _transform(self, df):
        try:
            logging.info("Starting data transformation")
            if 'store_id' not in df.columns:
                raise ValueError("'store_id' column is missing in the DataFrame")

            df['dayofweek'] = df.index.get_level_values(0).dayofweek
            df['day'] = df.index.get_level_values(0).day
            df['month'] = df.index.get_level_values(0).month
            df['is_weekend'] = df['dayofweek'].apply(lambda x: 1 if x >= 5 else 0)
            df['is_weekend'] = df['is_weekend'].astype('int')
            
            # ✅ FIX: Use global start_date instead of local 0th index
            df['days_since_start'] = (df.index.get_level_values(0) - self.start_date).days.astype('int')

            df['lag_1'] = df.groupby('store_id')['sales'].shift(1).fillna(method='bfill')
            df['lag_7'] = df.groupby('store_id')['sales'].shift(7).fillna(method='bfill')
            df['lag_14'] = df.groupby('store_id')['sales'].shift(14).fillna(method='bfill')

            encoder = OneHotEncoder(sparse_output=False, drop='first')
            agg_encoded = encoder.fit_transform(df[['store_id']])
            df[encoder.get_feature_names_out(['store_id'])] = agg_encoded
            df.drop(columns=['store_id'], inplace=True)

            logging.info("Data transformation completed")
            return df
        except Exception as e:
            logging.error(f"Error in data transformation: {e}")
            raise CustomException(e, sys)

    def initiate_data_transformation(self):
        try:
            logging.info("Data transformation started")
            raw_data = pd.read_csv(self.data_transformation_config.train_path)

            aggregated_data = self._aggregate(raw_data)
            
            # ✅ SET GLOBAL START DATE
            self.start_date = aggregated_data.index.min()

            min_date = aggregated_data.index.min()
            max_date = aggregated_data.index.max()
            split_date = min_date + (max_date - min_date) * 0.8

            train_data = aggregated_data[aggregated_data.index < split_date]
            test_data = aggregated_data[aggregated_data.index >= split_date]

            X_train = self._transform(train_data)
            X_test = self._transform(test_data)

            y_train = X_train['sales'].copy()
            y_test = X_test['sales'].copy()
            X_train.drop(columns=['sales'], inplace=True)
            X_test.drop(columns=['sales'], inplace=True)

            artifact_dir = os.path.dirname(self.data_transformation_config.train_path)
            os.makedirs(artifact_dir, exist_ok=True)

            X_train_path = os.path.join(artifact_dir, "X_train.csv")
            X_test_path = os.path.join(artifact_dir, "X_test.csv")
            y_train_path = os.path.join(artifact_dir, "y_train.csv")
            y_test_path = os.path.join(artifact_dir, "y_test.csv")

            X_train.to_csv(X_train_path, index=False)
            X_test.to_csv(X_test_path, index=False)
            y_train.to_csv(y_train_path, header=['sales'], index=False)
            y_test.to_csv(y_test_path, header=['sales'], index=False)

            logging.info("Data transformation completed and files saved")
            return (X_train_path, X_test_path, y_train_path, y_test_path)

        except Exception as e:
            logging.error(f"Error in data transformation: {e}")
            raise CustomException(e, sys)


if __name__ == "__main__":
    data_transformation = DataTransformation()
    train_path = data_transformation.data_transformation_config.train_path
    test_path = data_transformation.data_transformation_config.test_path
    data_transformation.initiate_data_transformation()
