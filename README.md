StockerLens 📈
Empowering retail investors with AI-driven stock market insights. StockerLens lets you predict stock prices, analyze news sentiment, classify chart trends, and query financial documents with StockGPT, a smart Retrieval-Augmented Generation (RAG) system. Upload earnings reports, ask questions like “Why did TSLA’s stock rise?”, and get answers backed by your documents and real-time web data.
🌟 Star and contribute to shape the future of retail investing!
Features

Stock Price Prediction: Forecast tomorrow’s stock prices using machine learning models (LSTM, Temporal Fusion Transformer) with data from Yahoo Finance or EOD APIs.
News Sentiment Analysis: Gauge market mood with NLP-powered analysis of news articles (e.g., positive/negative for AAPL).
Chart Trend Classification: Upload stock chart images to detect Up, Down, or Flat trends using computer vision or rule-based methods.
StockGPT: Query uploaded documents (PDF, TXT, DOCX) with AI, combining local knowledge stored in Qdrant with web searches via Firecrawl. Powered by Agno and OpenAI’s GPT-4o.

Tech Stack

Backend: FastAPI, Agno (RAG), Qdrant (vector database), Redis (caching), LangChain (document processing).
Machine Learning: PyTorch, Darts, pandas, SentenceTransformers.
Frontend: HTML, JavaScript, Tailwind CSS, Jinja2 templates.
Infrastructure: Docker, Qdrant Cloud, Redis Labs.
APIs: Firecrawl (web scraping), OpenAI (GPT-4o), Hugging Face (embeddings).

Project Structure
stockerlens/
├── app/
│   ├── api/
│   │   ├── main.py           # FastAPI app
│   ├── templates/
│   │   ├── sample.html       # Home page
│   │   ├── stockgpt.html     # StockGPT page
├── src/
│   ├── utils/
│   │   ├── logger.py         # Logging
│   ├── stock_price/
│   │   ├── pipeline/
│   │   │   ├── predict_pipeline.py  # Price prediction
│   ├── sentiment_analysis/
│   │   ├── pipeline/
│   │   │   ├── predict_pipeline.py  # Sentiment analysis
│   ├── chart_trend/
│   │   ├── pipeline/
│   │   │   ├── predict_pipeline.py  # Chart trend classification
│   ├── stockgpt/
│   │   ├── pipeline/
│   │   │   ├── rag_pipeline.py      # StockGPT RAG
│   │   ├── ingestion.py            # Document processing
│   │   ├── search.py               # Firecrawl web search
│   │   ├── agent.py                # Agno RAG agent
│   ├── common/
│   │   ├── config.py               # Configuration
│   │   ├── logging.py              # Agno logger
├── logs/
│   ├── app.log                     # App logs
│   ├── stockgpt.log                # StockGPT logs
├── tmp/
│   ├── agno_workflows.db           # Agno SQLite
├── Dockerfile                      # Container setup
├── requirements.txt                # Dependencies
├── .env                            # Environment variables

Prerequisites

Docker: For containerized setup.
Python 3.12: If running locally without Docker.
API keys for:
Firecrawl (web scraping)
OpenAI (GPT-4o)
Hugging Face (embeddings)



Setup Instructions

Clone the Repository:
git clone https://github.com/your-username/stockerlens.git
cd stockerlens


Set Up Environment Variables:Create a .env file in the root directory:
FIRECRAWL_KEY=your_firecrawl_key
OPENAI_API_KEY=your_openai_key
HUGGINGFACE_API_TOKEN=your_hf_token
QDRANT_URL=http://localhost:6333
REDIS_HOST=localhost
REDIS_PORT=6379


Run with Docker:

Build and run the container:docker build -t stockerlens .
docker run -d -p 8000:8000 --env-file .env stockerlens


Access the app at http://localhost:8000.


Run Locally (without Docker):

Install dependencies:pip install -r requirements.txt


Start Qdrant and Redis:docker run -d -p 6333:6333 qdrant/qdrant
docker run -d -p 6379:6379 redis


Run the FastAPI app:python -m app.api.main




Access the App:

Home: http://localhost:8000
StockGPT: http://localhost:8000/chat



Usage

Home Page (/sample.html):

Select a stock (e.g., AAPL) to predict its price.
Enter a stock symbol for news sentiment analysis.
Upload a chart image to classify its trend (Up/Down/Flat).
Click “Chat with StockGPT” to access the RAG system.


StockGPT Page (/stockgpt.html):

Upload a financial document (PDF, TXT, DOCX, e.g., TSLA earnings report).
Ask questions like “What are TSLA’s Q2 earnings?”.
Get responses combining document insights and web data (e.g., from Yahoo Finance, Reuters).



Example:

Upload tsla_earnings.pdf.
Query: “Why did TSLA’s stock rise in Q2 2025?”
Response: “TSLA’s stock rose due to 20% revenue growth from record deliveries [Source: Document]. Web sources cite strong EV demand [Source: finance.yahoo.com].”

Current Development Focus

StockGPT RAG: Enhancing the RAG system to persist the Qdrant vector database across FastAPI endpoints (/chat/upload to /chat/query) for seamless document querying.
Integration: Unifying price prediction, sentiment, and chart analysis with StockGPT for richer insights.
Scalability: Adding multi-user support with session-based knowledge bases.

Contributing
We welcome contributions! To get started:

Fork the repository.
Create a branch (git checkout -b feature/your-feature).
Commit changes (git commit -m "Add your feature").
Push to your fork (git push origin feature/your-feature).
Open a Pull Request.

Ideas for Contributions:

Optimize RAG performance (e.g., faster embeddings, Firecrawl efficiency).
Add new document formats (e.g., CSV, Markdown).
Enhance frontend with query history or document previews.
Implement session-based vector databases for multi-user support.

License
MIT License - Feel free to use, modify, and distribute.
Contact
Have questions or ideas? Open an issue or reach out via [your-email@example.com].

StockerLens: Your all-in-one tool for smarter investing. Join us to build the future of retail finance!
