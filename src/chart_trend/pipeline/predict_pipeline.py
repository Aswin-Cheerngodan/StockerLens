from fastapi import UploadFile
from typing import Optional
from src.chart_trend.components.data_ingestion import DataIngestion
from src.chart_trend.components.data_preprocessing import DataPreprocessor
from src.chart_trend.components.chart_classifier import ChartClassifier

from src.utils.logger import setup_logger


logger = setup_logger(__name__, r"logs/chart_trend.log")


class TrendClassifier:
    """Executes the prediction pipeline for chart trend classification."""
    def __init__(self, file:UploadFile) -> None:
        """Initialize with the file to be used for classification.
        Args:
            file (img): Image file for the classification.
        """
        self.file = file

    def classify(self) -> Optional[str]:
        """Executes the entire pipeline.
        Returns:
            Optional[str]: Classified class (Downtrend or Uptrend). None if classification fails.
        """
        try:
            data_ingestor = DataIngestion()
            file_path = data_ingestor.ingest_image(self.file)
            logger.info(f"File path saved and updated {file_path}")

            preprocessor = DataPreprocessor(file_path)
            img_array = preprocessor.preprocess()
            logger.info(f"Image preprocessing completed {img_array.shape}")

            classifier = ChartClassifier()
            trend = classifier._classify(img_array)
            logger.info(f"Image classification completed.")
             
            return trend
        except Exception as e:
            logger.error(f"Error while image classification.")
            return None