from fastapi import APIRouter, Request, Form, Depends, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,JSONResponse
import markdown
from src.stockgpt.pipeline.rag_pipeline import RAGHandler
from src.stockgpt.components.web_search_scrape import WebSearchandScraper
from src.stockgpt.components.data_ingestion import DataIngestion
from src.utils.logger import setup_logger


logger = setup_logger(__name__, "logs/app.log")

stockgpt_router = APIRouter(tags=["stockgpt"])
templates = Jinja2Templates(directory="app/templates")

@stockgpt_router.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    """Render StockGPT chat page"""
    logger.info("Rendered the page for StockGPT")
    return templates.TemplateResponse("stockgpt.html", {"request": request})

@stockgpt_router.post("/chat/upload")
async def create_vector_db(request: Request, file: UploadFile = File(...)):
    try:
        logger.info(f"Processing started for stockgpt.")
        data_ingestor = DataIngestion()
        data_ingestor.ingest_image(file=file)
        vector_db = data_ingestor.document_loader()
        request.app.state.vector_db = vector_db
        
        contents = await file.read()
        response = f"Received document with {len(contents)} bytes "
        
        return {"status": "success", "response": response}
    except Exception as e:
        logger.error(f"Error while creating vector database: {str(e)}")
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@stockgpt_router.post("/chat/query")
async def query_stockgpt(request: Request, query: str = Form(...)):
    try:
        vector_db = request.app.state.vector_db
        web_searcher = WebSearchandScraper()
        web_res = web_searcher.web_searcher_agent(query)
        rag = RAGHandler()
        response = rag.rag_generator(query, vector_db, web_res)
        logger.info(f"response got \n{response}")
        response = markdown.markdown(response)
        return {"status": "success", "response": response}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": "Failed to generate response"})
    
