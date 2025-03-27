from fastapi import APIRouter, Request, Form, Depends, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from src.stock_price.components.price_predict import PricePredictor

home_router = APIRouter(tags=["home"])
templates = Jinja2Templates(directory="app/templates")

@home_router.get("/", response_class=HTMLResponse)
async def stock_price_page(request: Request):
    """Render stock price prediction page"""
    return templates.TemplateResponse("index.html", {"request": request})

# stock price prediction endpoint
@home_router.post("/price")
async def predict_stock_price(stock_symbol: str = Form(...)):
    try:
        pass
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
# sentiment analysis endpoint
@home_router.post("/sentiment")
async def analyze_news_sentiment(stock: str = Form(...)):
    try:
        pass
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
# chart trend analyzer endpoint
@home_router.post("/chart")
async def analyze_chart_trend(file: UploadFile = File(...)):
    try:
        pass
    except Exception as e:
        return {"status": "error", "message": str(e)}
