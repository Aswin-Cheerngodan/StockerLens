from typing import Optional
import requests
from bs4 import BeautifulSoup
import time

from src.utils.logger import setup_logger


logger = setup_logger(__name__, r"logs/sentiment_analysis.log")


class WebScraper:
    """Class for handling web scraping."""
    def __init__(self, symbol: str):
        """Initialization of the class for web scraping.
        
        Args:
            symbol (str): Stock symbol for the sentiment analysis.
        """
        self.symbol = symbol.lower()
        logger.info(f"stock symbol updated {self.symbol}")


    def scrape_news(self,url: str, tag: str, class_name: str) -> Optional[str]:
        """Script for scraping news from the websites.

        Args:
            url (str): url of the website that contains news. (yahoofinance, cnbc, fiviz)
            tag (str): HTML tag that holds the news in the respective website.
            class_ (str): Class name of the tag that holds the news.

        Returns:
            Optional[str]: Scraped news data of the stock from the given url. None if scraping fails.
        """
        try:
            headers = {"User-Agent": "Mozilla/5.0"}    # To avoid bot detection
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                logger.error(f"failed to fetch {url} with status code {response.status_code}")
                return None
            
            soup = BeautifulSoup(response.text, "html.parser")
            headlines = soup.find_all(tag, class_=class_name)
            logger.info(f"Web scraping completed for {url}")
            # Extracting all the text and putting into a list.
            news_data = []
            x = 12 if len(headlines)>12 else len(headlines)
            for i in range(x):
                title = headlines[i].get_text()
                news_data.append(title)
            logger.info(f"Data extraction completed for {url}")
            time.sleep(1)

            return news_data
        except Exception as e:
            logger.error(f"Error while web scraping: {str(e)}")
            return None
        
    
    def scrape_all(self) -> Optional[str]:
        """Scrape news from all the websites.

        Returns:
            news_data (str): list of news data about a particular stock from all websites.
        """
        site1 = {
            "url": f"https://finance.yahoo.com/quote/{self.symbol}/news/",
            "tag": "h3",
            "class": "clamp"
            }
        site2 = {
            "url": f"https://www.cnbc.com/quotes/{self.symbol}?tab=news",
            "tag": "a",
            "class": "LatestNews-headline"
                 }
        site3 = {
            "url": f"https://finviz.com/quote.ashx?t={self.symbol}&p=d",
            "tag": "a",
            "class": "tab-link-news"
            }

        sites = [site1, site2, site3]
        try:
            news_data = []
            for site in sites:
                news_data.extend(self.scrape_news(url=site["url"], tag=site["tag"], class_name=site["class"]))
            logger.info(f"Web scraping from all websites completed with number of newses {len(news_data)}")
            return news_data
        except Exception as e:
            logger.error(f"Error while scraping from all websites: {str(e)}")
            return None


# if __name__=="__main__":
#     scraper = WebScraper("AAPL")
#     news_data = scraper.scrape_all()
#     print(len(news_data))
#     logger.debug(f"first 5 headlines of the news {news_data[:5]}")


        


        
    
        