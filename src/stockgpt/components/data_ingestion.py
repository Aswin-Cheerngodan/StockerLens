from typing import Optional
from fastapi import UploadFile
from PIL import Image
from pathlib import Path
import shutil
import uuid

from src.utils.logger import setup_logger


logger = setup_logger(__name__, r"logs/chart_trend.log")


class DataIngestion:
    """Class to handle data ingestion for RAG."""
    def __init__(self, upload_dir: Path = Path(r"app\static\uploads")):
        """ Initialize with image directory.
        
        Args:
            upload_dir (Path): Directory to store uploaded files. Defaults to r"app\static\ploads"
        """
        self.upload_dir = upload_dir
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Intialized Data ingestion for chart trend classification with upload_dir: {upload_dir}")

    
    def ingest_image(self, file: UploadFile):
        """Accept, save and validate the file.
        
        Args:
            file (UploadFile): Uploaded file from FastAPI.

        Retruns:
            file :Path for the file or None.
        """
        try:
            # Save the file
            unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
            file_path = self.upload_dir / unique_filename
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            logger.info(f"file saved successfully: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"file saving failed: {str(e)}", exc_info=True)
            return None