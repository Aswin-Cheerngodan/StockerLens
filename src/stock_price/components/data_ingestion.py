import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
import os

import pandas as pd
import requests
import yfinance as yf
from requests.exceptions import RequestException
from dotenv import load_dotenv
from src.utils.logger import setup_logger


load_dotenv()
# Initialize logger
logger = setup_logger(__name__, "logs/stock_price.log")


class DataIngestion:
    """Class to handle data ingestion for stock price and sentiment data."""
    def __init__(self, symbol: str) -> None:
        """Initialize with user selected stock symbol

        Args: 
            symbol (str): Stock ticker symbol

        Raises:
            ValueError: If symbol is invalid or missing
        """

        api_token = os.getenv("EODHD_API_TOKEN")

        if not symbol:
            logger.error("Stock symbol must be a non-empty string.")
            raise ValueError("Stock symbol must be a non-empty string.")
        if not api_token:
            logger.error("EODHD API token missing.")
            raise ValueError("EODHD API token required.")
        
        self.ticker = symbol
        self.api_token = api_token
        # Set dates: 30 days before today to today
        self.end_date = datetime.today().strftime("%Y-%m-%d")
        self.start_date = (datetime.today() - timedelta(days=30)).strftime("%Y-%m-%d")

        logger.info(f"Initialized ingestion for {symbol} from {self.start_date} to {self.end_date}")


    def fetch_stock_prices(self):
        """Fetch sotck price data from Yahoo Finance for the last 30 days.

        Returns:
            Optional[pd.DataFrame]: OHLCV data or None if fetching fails.
        """
        logger.info(f"Fetching stock prices for {self.ticker} from {self.start_date} to {self.end_date}")
        try:
            stock_data = yf.download(
                tickers=self.ticker,
                start=self.start_date,
                end=self.end_date,
                progress=False
            )
            if stock_data.empty:
                logger.warning(f"No stock data for {self.ticker}")
                return None
            #dropping unnecessary row
            stock_data = stock_data.droplevel(1, axis=1)
            logger.debug(f"Stock data sample:\n{stock_data.tail().to_string()}")
            # Converting into DataFrame
            stock_df = pd.DataFrame(stock_data, index=stock_data.index)
            # Reset the index to make 'Date' a column
            stock_df.reset_index(inplace=True)
            # Rename the 'index' column to 'Date'
            stock_df.rename(columns={'index': 'date'}, inplace=True)
            return stock_df
        except Exception as e:
            logger.error(f"Stock price fetch failed: {str(e)}")
            return None
        

    def fetch_sentiment_data(self):
        """Fetch sentiment data from EODHD API for the last 30 days.

        Returns:

        """
        eod_ticker = f"{self.ticker}.US"
        url = f"https://eodhd.com/api/sentiments?s={self.ticker.lower()}.us&from={self.start_date}&to={self.end_date}&api_token={self.api_token}&fmt=json"

        logger.info(f"Fetching sentiment scores for {self.ticker}")
        try:
            response = requests.get(url, timeout=10).json()
            sentiment_data = response
            if not sentiment_data:
                logger.warning(f"No sentiment data for {self.ticker}")
                return None
            
            # Converting into DataFrame
            symbol = list(sentiment_data.keys())[0]
            data = sentiment_data[symbol]
            sentiment_df = pd.DataFrame(data)
            logger.debug(sentiment_df)
            return sentiment_data
        except RequestException as e:
            logger.error(f"Sentiment fetch failed: {str(e)}")


    def merge_all_data(self):
        """Fetch both stock price and sentiment data for the last 30 days.
        Merge them according to the date.

        Returns: 

        """
        logger.info("Starting full data ingestion")
        stock_data = self.fetch_stock_prices()
        sentiment_data = self.fetch_sentiment_data()





if __name__=="__main__":
    obj = DataIngestion("AAPL")
    obj.fetch_stock_prices()
    obj.fetch_sentiment_data()

    