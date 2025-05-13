from typing import Optional
from fastapi import UploadFile
from PIL import Image
from pathlib import Path
import shutil
import uuid

from src.utils.logger import setup_logger


logger = setup_logger(__name__, r"logs/chart_trend.log")


class DataIngestion:
    """Class to handle data ingestion for chart trend classification."""
    def __init__(self, upload_dir: Path = Path(r"app/static/uploads")):
        """ Initialize with image directory.
        
        Args:
            upload_dir (Path): Directory to store uploaded images. Defaults to r"app/static/uploads"
        """
        self.upload_dir = upload_dir
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Intialized Data ingestion for chart trend classificatio with upload_dir: {upload_dir}")

    
    def ingest_image(self, file: UploadFile):
        """Accept, save and validate the image.
        
        Args:
            file (UploadFile): Uploaded image from FastAPI.

        Retruns:
            file : Validated image file or None.
        """
        try:
            # Validate file type
            if not file.content_type.startswith("image/"):
                logger.error(f"Invalid file type: {file.content_type}. Expected image.")
                return None

            # Save the file
            unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
            file_path = self.upload_dir / unique_filename
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            logger.info(f"Image ingested successfully: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Image ingestion failed: {str(e)}", exc_info=True)
            return None
        
        
        


# if __name__=="__main__":
#     data_ingestor = DataIngestion()
#     data_ingestor.ingest_image("NO")