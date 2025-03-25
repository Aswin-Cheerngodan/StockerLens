import logging
from typing import Optional, Tuple
import os

import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import joblib

from src.stock_price.components.data_ingestion import DataIngestion
from src.stock_price.components.data_preprocessing import DataPreprocessor
from src.utils.logger import setup_logger

logger = setup_logger(__name__, "logs/stock_price.log")


class PricePredictor:
    """Class to predict next day's price using a Trained LSTM model."""

    def __init__(
            self,
            ticker: str = "MSFT",
            model_path: str = "artifacts\models\stock_price",
            scaler_path: str = "artifacts\preprocessors\stock_price",
            timesteps: int = 10,
    ) -> None:
        """
        Intialize the price predictor with model path and scaler path

        Args:
            ticker (str): Name of the stock ticker. Defaults to MSFT(microsoft)
            model_path (str): Path to the folder containing the stock price prediction models.
            scaler_path (str): Path to the folder containing the scaler for the stock price.
            timesteps (int): Number of past days used for prediction. Defaults to 10.
        """

        self.model_path = model_path
        self.scaler_path = scaler_path
        self.timesteps = timesteps
        self.ticker = ticker
        self.stock_name_map = {
            "MSFT":"microsoft",
            "AAPL":"apple"
        }

    def _load_model(self) -> Optional['tensorflow.keras.Model']:
        """Load the trained LSTM model

        Returns: 
            Optional[tensorflow.keras.Model]: Loaded model or None if loading fails.
        """
        try:
            stock_name = self.stock_name_map[self.ticker]
            model_path = os.path.join(self.model_path, f"{stock_name}_model.keras")
            model = load_model(model_path)
            logger.info(f"Loaded LSTM model from {model_path}")
            return model
        except Exception as e:
            logger.error(f"Failed to load the model from : {model_path}")
            return None
        
    


