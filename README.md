# StockerLens 📈

**Empowering retail investors with AI-driven stock market insights.**

StockerLens lets you **predict stock prices**, **analyze news sentiment**, **classify chart trends**, and **query financial documents** with **StockGPT**, a smart Retrieval-Augmented Generation (RAG) system also powered with web search agent. Upload earnings reports, ask questions like _“Why did TSLA’s stock rise?”_, and get answers backed by your documents and real-time web data.

🌟 **Star and contribute to shape the future of retail investing!**

---

## 🔍 Features

- **Stock Price Prediction**: Forecast today’s closing stock prices using ML models like Bidirectional-LSTM with data from Yahoo Finance or EOD APIs.

- **News Sentiment Analysis**: Analyze the tone of news articles (e.g., Very Positive for AAPL) using NLP.

- **Chart Trend Classification**: Upload stock chart images to detect Up, or Down trends using computer vision.

- **StockGPT**: Ask financial questions and query uploaded documents (PDF, TXT, DOCX) using a RAG system powered by Agno, Groq, Faiss and duckduckgo-search.

---

## 🧠 Tech Stack

**Backend**: FastAPI, Agno (RAG), Faiss-cpu (vector DB), LangChain  
**Machine Learning**: PyTorch, TensorFlow, pandas, Transformers, numpy  
**Frontend**: HTML, JavaScript, Tailwind CSS, Jinja2  
**Infrastructure**: Docker  
**APIs**: Mistralai (embeddings), EODHD (price prediction data), Groq (stockGPT)

---


---

## ✅ Prerequisites

- **Docker** (recommended)
- **Python 3.12** (if running locally)
- **API Keys**:
  - Mistralai (embeddings)
  - Groq (LLM)
  - EODHD (stock data)

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Aswin-Cheerngodan/StockerLens.git
cd stockerlens
```
### 2. Set Up Environment Variables
Create a .env file:

EODHD_API_TOKEN=your_eodhd_token     
GROQ_API_KEY=your_groq_key  
MISTRAL_API_KEY=your_mistral_key   


### 3. Run with Docker 
```bash
docker build -t stockerlens .
docker run -d -p 8000:8000 --env-file .env stockerlens
```

### 4. Run Locally (Without Docker)
```bash
python -m venv myenv
myenv\Scripts\activate

pip install -r requirements.txt
python -m app.api.main
```

### 🌐 Access the App
Home Page: http://localhost:8000   
StockGPT Page: http://localhost:8000/chat   

### 📬 Contact
Questions or suggestions? Open an issue or contact me at aachu8966@gmail.com.





