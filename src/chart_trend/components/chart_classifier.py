from typing import Optional
from pathlib import Path
from tensorflow.keras import Model
from tensorflow.keras.models import load_model
import numpy as np

from src.utils.logger import setup_logger


logger = setup_logger(__name__, "logs/chart_trend.log")


class ChartClassifier:
    """Class handles chart classification."""
    def __init__(self, model_path: Path = Path(r"artifacts/models/chart_trend/chart_trend_model.keras")):
        """Intialize with path of the model.
        
        Args:
            model_path (Path): Path to the chart trend classifier model. Defaults to "artifacts\models\chart_trend\chart_trend_model.keras"
        """
        self.model_path = model_path
        self.classes = ["Downtrend", "Uptrend"]


    def _load_model(self) -> Model:
        """Loading the CNN model for chart trend classification from model_path

        Returns (Model): Loaded CNN model or None if loading fails.
        """
        try:
            model = load_model(self.model_path)
            logger.info(f"CNN model loaded from {self.model_path}")
            return model
        except Exception as e:
            logger.error(f"Error while loading the model :{str(e)}")
            return None
        
    def _classify(self, data: np.ndarray) -> Optional[str]:
        """Classifies the input data into downtrend and uptrend.
        Args:
            data (np.ndarray): Numpy array with shape (1, 224, 224, 3) for matching the input shape of the model.

        Returns:
            Optional (str): Downtrend or Uptrend. None if prediction fails.
        """
        try:
            model = self._load_model()
            pred = model.predict(data)
            if not pred.any():
                logger.error(f"Prediction failed.")
                return None
            trend = self.classes[np.argmax(pred)]
            return trend
        except Exception as e:
            logger.error(f"Error while prediction: {str(e)}", exc_info=True)
            return None

        