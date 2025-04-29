from typing import Optional, List
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools

from src.utils.logger import setup_logger
import os
from dotenv import load_dotenv
load_dotenv()


logger = setup_logger(__name__,"logs/stockgpt.log")


class WebSearchandScraper:
    """Class for handling web search for the given query."""
    def __init__(self):
        """Intializer for the web search and scraping class."""

    
    def web_searcher_agent(self, query: str) -> Optional[str]:
        """searches in the web and finds the best results for the query.
        
        Args:
            query (str): query for the web search.
        Returns:
            Optional[str]: Web search results if completed. None if websearch fails.
        """
        try:
            web_search_agent = Agent(
                name="Web Search Agent",
                role="Search the web for relevant information based on user queries",
                model=Groq(id="deepseek-r1-distill-llama-70b"),  
                tools=[DuckDuckGoTools()],  # Use DuckDuckGo for web searches
                instructions="Search the web for the given query, extract top results, and summarize them.",
                show_tool_calls=True,
                markdown=True,
            )
            
            response = web_search_agent.run(query)
            return response
        except Exception as e:
            logger.error(f"Error while web searching using agno : {str(e)}")
            return None
        
    


if __name__=="__main__":
    websearchscrape = WebSearchandScraper()
    response = websearchscrape.web_searcher_agent("Today ipl match details")
    logger.info(response.content)
    # print(response)

        