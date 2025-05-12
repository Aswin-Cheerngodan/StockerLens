from langchain_text_splitters.character import RecursiveCharacterTextSplitter  
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS 
from typing import Optional
from fastapi import UploadFile
import os
from pathlib import Path
import shutil
import uuid

from src.utils.logger import setup_logger


logger = setup_logger(__name__, r"logs/chart_trend.log")


class DataIngestion:
    """Class to handle data ingestion for RAG."""
    def __init__(self, upload_dir: Path = Path(r"app/static/uploads")):
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
            self.file_path = file_path
        except Exception as e:
            logger.error(f"file saving failed: {str(e)}", exc_info=True)
            return None
        
    def document_loader(self):
        """Checks and Loads the document from the file path.

        Returns:
            Optional[file]: Returns the loaded file for the RAG. None if fails
        """
        try:
            # Checking the document
            str_file_path = str(self.file_path)
            if str_file_path.endswith(".pdf"):
                loader = PyPDFLoader(self.file_path)
                logger.info(f"pdf file loader updated from path: {self.file_path}")
            elif str_file_path.endswith(".txt"):
                loader = TextLoader(self.file_path)
                logger.info(f"txt file loader updated from path: {self.file_path}")
            # Loading the document
            documents = loader.load()
            logger.info("document loaded for RAG")
            if os.path.exists(self.file_path):
                os.remove(self.file_path)
                logger.info(f"{self.file_path} deleted.")
            # Split document for storing in vector database
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            docs = text_splitter.split_documents(documents)
            logger.info(f"splitted the documents.")
            # Create and store documents in vector database
            vector_db=FAISS.from_documents(documents, MistralAIEmbeddings())
            logger.info(f"Vector database created from documents.")
            
            return vector_db
        except Exception as e:
            logger.error(f"Error while creating vector database from documents: {str(e)}")
            return None 