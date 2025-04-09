from pathlib import Path
from typing import Optional
import os
import numpy as np
import cv2

from src.utils.logger import setup_logger

logger = setup_logger(__name__, "logs/chart_trend.log")


class DataPreprocessor:
    """Class to preprocess the data for the model input."""
    def __init__(self, file_path: Path):
        """ Initialize with file path of the image for preprocessing.

        Args:
            file_path (str): path of the image.
        
        """
        self.file_path = file_path

    
    def preprocess(self, image_size=(224, 224)) -> Optional[np.ndarray]:
        """ Preprocess the image for CNN input.

        Returns:
            Optional[np.ndarray]: Preprocessed image array.shape:(1, height, width, channels), or None if preprocessing fails.
        """
        try:
            # Open and resize image
            img = cv2.imread(self.file_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            resized_image = cv2.resize(img, image_size)
            img_normalized = resized_image / 255.0
            img_array = np.expand_dims(img_normalized, axis=0)
            logger.debug(f"Preprocessed image shape: {img_array.shape}")
            if os.path.exists(self.file_path):
                os.remove(self.file_path)
                print(f"{self.file_path} deleted.")
            return img_array
        except Exception as e:
            logger.error(f"Image preprocessing failed: {str(e)}", exc_info=True)
            return None