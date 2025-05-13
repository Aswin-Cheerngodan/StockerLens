from typing import Optional, List
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import re
from pathlib import Path

from src.utils.logger import setup_logger

logger = setup_logger(__name__,r"logs/sentiment_analysis.log" )


class SentimentAnalyzer:
    """Class handles the data preprocessing and sentiment analysis."""
    def __init__(self, model_path: Path =Path(r"artifacts/models/sentiment_analysis/sentiment_model")):
        """Intializing the class for sentiment analysis.
        
        Args:
            model_path (Path): Path of the sentiment analysis model
        """
        self.model_path = model_path
        self.sentiment_map = {0:"Very Negative", 1:"Negative", 2:"Neutral", 3:"Positive", 4:"Very Positive"}


    def _data_preprocessing(self, data: List[str]) -> Optional[str]:
        """Cleaning and preprocessing news data for input to the model.
        
        Args:
            data (List[str]): Scraped news data as list of sentances.

        Returns:
            Optional[str]: Concatenated sentences string. None if preprocessing fails.
        """
        text = ", ".join(data)
        return text

    def _load_model(self):
        """Load the finbert model and tokenizer for sentiment analysis.
        
        Retrurns:
            Model : Loaded model. None if loading fails
            Tokenizer: Loaded tokenizer for the model
        """
        try:
            tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
            model.eval()
            logger.info(f"Model and tokenizer loaded from: {self.model_path}")
            return tokenizer, model
        except Exception as e:
            logger.error(f"Error while loading the tokenizer and model: {str(e)}", exc_info=True)
            return None
        
    
    def predict_sentiment(self, data: List[str]):
        """Predict the sentiment for the preprocessed data.
        
        Args:
            data (List[str]): Scraped news data.

        Returns:

        """
        try:
            data = self._data_preprocessing(data=data)
            tokenizer, model = self._load_model()

            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            model.to(device)

            inputs = tokenizer(
                data,
                return_tensors='pt',
                truncation=True,
                padding=True,
                max_length=512
            )
            inputs = {k: v.to(device) for k, v in inputs.items()}
            logger.info("Input query toknization done.")
            # Inference
            with torch.no_grad():
                outputs = model(**inputs)
                logits = outputs.logits
                probs = torch.softmax(logits, dim=1).cpu()
                predicted_idx = torch.argmax(probs, dim=1).item()
                sentiment = self.sentiment_map[predicted_idx]
            # logger.debug(f"inputs \n data {data} \n logits {logits}")
            logger.info(f"Predicted senitment of the news: {sentiment} with probability scores: {probs}")
            return sentiment
        except Exception as e:
            logger.error(f"Error while predicting sentiment: {str(e)}")
            return None
        


    








        