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
            model_path: str = r"artifacts/models/stock_price",
            scaler_path: str = r"artifacts/preprocessors/stock_price",
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
        self.model = self._load_model()


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
        

    def _prepare_data(self, data: pd.DataFrame) -> Optional[np.ndarray]:
        """Prepare the data for the LSTM prediction.
        
        Args:
            data (pd.DataFrame): Preprocessed data with features.

        Returns:
            Optional[np.ndarray]: 3D array (1, timesteps, features) for prediction, or None if prepration fails.
        """
        try:
            features = data.values[-self.timesteps:]
            X = np.array([features])
            logger.debug(f"Prepared input data:\n{X}")
            return X
        
        except Exception as e:
            logger.error(f"Failed to prepare input: {str(e)}")
            return None
        

    def predict_price(self) -> Optional[float]:
        """Predict next day's stock price for the given symbol.

        Args:
            None
        
        Returns:
            Optional[float]: Predicted stock price in dollars, or None if Prediction fails
        """
        logger.info(f"Starting Price prediction for {self.ticker}")

        try:
            ingestor = DataIngestion(symbol=self.ticker)
            merged_data = ingestor.merge_all_data()
            if merged_data is None:
                logger.error("Failed to fetch or merge data.")
                return None
            
            # Preprocessing
            preprocessor = DataPreprocessor(scaler_path=self.scaler_path)
            preprocessed_data = preprocessor.preprocess(symbol=self.ticker, merged_data=merged_data)
            if preprocessed_data is None:
                logger.error("Failed to preprocess data")
                return None
            
            # Preparing data for prediction
            X = self._prepare_data(preprocessed_data)
            if X is None:
                logger.error("Failed to prepare input for prediction.")
                return None
            
            # Predict normalized target
            normalized_pred = self.model.predict(X, verbose=0)[0]

            logger.debug(f"Normalized prediction: {normalized_pred}")

            stock_name = self.stock_name_map.get(self.ticker)
            scaler_path = os.path.join(self.scaler_path, f"{stock_name}_scaler.pkl")

            logger.info(f"Scaler path updated: {scaler_path}")

            # Inverse transforming the predicted data
            scaler = joblib.load(scaler_path)
            dummy = np.zeros((len(normalized_pred), 6))
            dummy[:, 0] = normalized_pred.flatten()
            predicted = scaler.inverse_transform(dummy)[:, 0]
            logger.debug(f"Predicted price: {predicted}")
            return round(predicted[0], 2)
        
        except Exception as e:
            logger.error(f"Price prediction failed: {str(e)}", exc_info=True)
            return None
        



# if __name__=="__main__":
#     symbol = "MSFT"

#     predictor = PricePredictor(ticker=symbol)
#     predicted_price = predictor.predict_price()

#     if predicted_price is not None:
#         print(f"Predicted Today's closing price for {symbol}: ${predicted_price}")
#     else:
#         print("Prediction failed. Check logs for details.")


    


