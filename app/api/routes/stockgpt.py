from fastapi import APIRouter, Request, Form, Depends, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,JSONResponse
from src.stockgpt.pipeline.rag_pipeline import RAGHandler
from src.stockgpt.components.web_search_scrape import WebSearchandScraper
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
        rag_handler = RAGHandler(file=file)
        vector_db = rag_handler.document_loader()
        request.app.state.vector_db = vector_db
        # Placeholder logic: Replace this with actual LLM-based pipeline
        contents = await file.read()
        response = f"Received document with {len(contents)} bytes "
        
        # Ideally, pass `contents` and `query` to a DocumentQA pipeline
        return {"status": "success", "response": response}
    except Exception as e:
        logger.error(f"Error while creating vector database: {str(e)}")
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@stockgpt_router.post("/chat/query")
async def query_stockgpt(request: Request, query: str = Form(...)):
    try:
        # Placeholder logic: Replace this with actual LLM-based pipeline
        vector_db = request.app.state.vector_db
        web_searcher = WebSearchandScraper()
        web_res = web_searcher.web_searcher_agent(query)
        rag = RAGHandler()
        response = rag.rag_generator(query, vector_db, web_res)
        logger.info(f"response got \n{response}")
        return {"status": "success", "response": response}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
    
