from fastapi import APIRouter, Request, Form, Depends, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from src.utils.logger import setup_logger


logger = setup_logger(__name__, "logs/app.log")

stockgpt_router = APIRouter(tags=["stockgpt"])
templates = Jinja2Templates(directory="app/templates")

@stockgpt_router.post("/process")
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