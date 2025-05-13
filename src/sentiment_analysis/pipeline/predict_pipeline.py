from typing import Optional
from src.sentiment_analysis.components.web_scraper import WebScraper
from src.sentiment_analysis.components.sentiment_analyzer import SentimentAnalyzer

from src.utils.logger import setup_logger


logger = setup_logger(__name__, r"logs/sentiment_analysis.log")


class SentimentPredictPipeline:
    """Pipeline class for sentiment prediction."""
    def __init__(self, symbol: str):
        """Initialize the pipeline
        
        Args
            symbol (str): Stock symbol for sentiment analysis.
        """
        self.symbol = symbol.lower()
        
    def predict(self):
        """Predict the sentiment of the stock."""
        # Web scraping
        webscraper = WebScraper(self.symbol)
        data = webscraper.scrape_all()
        # Sentiment analyzer
        analyzer = SentimentAnalyzer()
        pred = analyzer.predict_sentiment(data)
        
        return pred 
    

