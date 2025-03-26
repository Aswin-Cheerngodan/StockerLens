import logging
from typing import Optional
import os

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib

from src.stock_price.components.data_ingestion import DataIngestion
from src.utils.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__, "logs/stock_price.log")

class DataPreprocessor:
    """Class to preprocess the data for the model input"""

    def __init__(self, scaler_path: str = r"artifacts\preprocessors\stock_price") -> None:
        """Initialize the preprocessor with saved path of scaler.

        Args:
            scaler_path (str): Path to the saved scaler folder.
        """

        self.scaler_path = scaler_path
        self.scaler = None
        self.feature_columns = ['Open', 'Close', 'High', 'Low', 'Volume', 'normalized']

        logger.info(f"Initialized DataPreprocessor with scaler path: {scaler_path}")


    def load_scaler(self, symbol: str) -> StandardScaler:
        """Load an existing scaler.

        Args:
            symbol (str): stock symbol to fetch the respective scaler.

        Returns:
            StandardScaler: Loaded scaler object
        """
        # Updating scaler path based on the stock name
        stock_name_map = {
            "AAPL": "apple",
            "MSFT": "microsoft",
        }
        stock_name = stock_name_map.get(symbol)
        self.scaler_path = os.path.join(self.scaler_path, f"{stock_name}_scaler.pkl")

        logger.info(f"Scaler path updated: {self.scaler_path}")

        if os.path.exists(self.scaler_path):
            try:
                self.scaler = joblib.load(self.scaler_path)
                logger.info(f"Loaded scaler from {self.scaler_path}")

            except Exception as e:
                logger.error(f"Failed to load scaler: {str(e)}")
                self.scaler = None

        else:
            logger.warning(f"No scaler found at {self.scaler_path}")

        return self.scaler
    

    def preprocess(self,symbol: str, merged_data: pd.DataFrame) -> Optional[pd.DataFrame]:
        """Preprocess merged stock price and sentiment data for model input.

        Args:
            symbol (str): stock symbol (eg: AAPL)
            merged_data (pd.DataFrame): DataFrame from DataIngestion.merge_all_data with columns:
                'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'count', 'normalized'.

        Returns:
            Optional[pd.DataFrame]: Preprocessed DataFrame with normalized features and Target column,
                or None if preprocessing fails.
        """
        logger.info("Starting data preprocessing")

        if merged_data is None or merged_data.empty:
            logger.error("Input data is None or empty. Cannot preprocess")
            return None
        
        try:
            df = merged_data.copy()
            df['normalized'] = df['normalized'].fillna(0)
            df = df[self.feature_columns]
            # Standardizing features
            scaler = self.load_scaler(symbol=symbol)
            scaled_data = scaler.transform(df)  
            scaled_df = pd.DataFrame(scaled_data,columns=self.feature_columns)
            
            logger.info(f"Preprocessed data shape: {df.shape}")
            logger.debug(f"Preprocessed data sample:\n{df.head().to_string()}")

            return scaled_df
        
        except Exception as e:
            logger.error(f"Preprocessing failed: {str(e)}", exc_info=True)
            return None




# if __name__=="__main__":
#     dataingestor = DataIngestion("AAPL")
#     merged_data = dataingestor.merge_all_data()

#     preprocessor = DataPreprocessor()
#     logger.debug(preprocessor.preprocess("AAPL", merged_data))