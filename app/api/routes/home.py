from fastapi import APIRouter, Request, Form, Depends, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from src.utils.logger import setup_logger
from src.stock_price.pipeline.predict_pipeline import predictionPipeline
from src.chart_trend.pipeline.predict_pipeline import TrendClassifier
from src.sentiment_analysis.pipeline.predict_pipeline import SentimentPredictPipeline

logger = setup_logger(__name__, "logs/app.log")


home_router = APIRouter(tags=["home"])
templates = Jinja2Templates(directory="app/templates")

@home_router.get("/", response_class=HTMLResponse)
async def stock_price_page(request: Request):
    """Render stock price prediction page"""
    return templates.TemplateResponse("sample.html", {"request": request})

# stock price prediction endpoint
@home_router.post("/price")
async def predict_stock_price(stock_symbol: str = Form(...)):
    try:
        logger.info(f"Stock symbol: {stock_symbol}")
        predictor = predictionPipeline(symbol=stock_symbol)
        price = predictor.predict()
        logger.debug(price)
        margin_error = "0" 
        return {
            "status": "success",
            "stock_symbol": stock_symbol,
            "predicted_price": price,
            "margin_error": margin_error
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
# sentiment analysis endpoint
@home_router.post("/sentiment")
async def analyze_news_sentiment(stock: str = Form(...)):
    try:
        logger.info(f"Stock symbol: {stock}")
        pipeline = SentimentPredictPipeline(stock)
        pred = pipeline.predict() 
        return {
            "status": "success",
            "stock_symbol": stock,
            "sentiment": pred
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
# chart trend analyzer endpoint
@home_router.post("/chart")
async def analyze_chart_trend(file: UploadFile = File(...)):
    """Handle chart image upload and predict the trend."""
    # Ingest the image
    classifier = TrendClassifier(file)
    trend = classifier.classify()
    trend = str(trend)
    return {
            "status": "success",
            "filename": file.filename,
            "trend": trend
        }
