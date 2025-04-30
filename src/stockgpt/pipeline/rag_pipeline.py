from langchain_groq import ChatGroq
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters.character import RecursiveCharacterTextSplitter  
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS 
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from src.stockgpt.components.web_search_scrape import WebSearchandScraper
from src.stockgpt.components.data_ingestion import DataIngestion
from src.utils.logger import setup_logger
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

groq_api_key=os.environ['GROQ_API_KEY']
mistral_api_key=os.environ["MISTRAL_API_KEY"]
logger = setup_logger(__name__, "logs/stockgpt.log")

class RAGHandler:
    """Class for hanlding the RAG Pipeline."""
    def __init__(self, file=None):
        """Intializer for the RAG Pipeline
        
        Args:
        Returns:
        """
        if file:
            data_ingestor = DataIngestion()
            self.file_path = data_ingestor.ingest_image(file)
    
    def document_loader(self):
        """Checks and Loads the document from the file path.

        Args:
            file_path (Path): Path to the file containing for the rag.
        Returns:
            Optional[file]: Returns the loaded file for the RAG. None if fails
        """
        try:
            str_file_path = str(self.file_path)
            if str_file_path.endswith(".pdf"):
                loader = PyPDFLoader(self.file_path)
                logger.info(f"pdf file loader updated from path: {self.file_path}")
            elif str_file_path.endswith(".txt"):
                loader = TextLoader(self.file_path)
                logger.info(f"txt file loader updated from path: {self.file_path}")

            documents = loader.load()
            logger.info("document loaded for RAG")

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            docs = text_splitter.split_documents(documents)
            logger.info(f"splitted the documents.")

            vector_db=FAISS.from_documents(documents, MistralAIEmbeddings())
            logger.info(f"Vector database created from documents.")
            
            return vector_db
        except Exception as e:
            logger.error(f"Error while creating vector database from documents: {str(e)}")
            return None
        
    def rag_generator(self, query: str, vector_db, web_result):
        """Splits and make chunks of the documents for storage.
        Args:
            query: User's query to the system.
            web_result: web search result.
            documents: Loaded documents of file.
        Returns:
            docs: Splitted documents. None if splitting fails
        """
        try:
            llm=ChatGroq(groq_api_key=groq_api_key,
                         model_name="mistral-saba-24b")
            messages = [
                SystemMessagePromptTemplate.from_template(
                    "You are a helpful assistant that only answers based on the given context only."
                ),
                HumanMessagePromptTemplate.from_template(
                    "<context>\n{context}\n</context>\nQuestion: {input}"
                ),
                SystemMessagePromptTemplate.from_template(
                    f"This is the result from web search of this query {{web_result}}"
                ),
                SystemMessagePromptTemplate.from_template(
                    "Provide raw text only. Avoid using **bold**, *, or any markdown formatting in the response."
                )
            ]

            prompt = ChatPromptTemplate.from_messages(messages)
            logger.info("Prompt updated for the RAG system.")

            document_chain = create_stuff_documents_chain(llm, prompt)
            logger.info("created document chain.")
            
            retriever=vector_db.as_retriever()
            logger.info("retriever updated for RAG.")

            retrieval_chain=create_retrieval_chain(retriever,document_chain)
            logger.info("created retrieval chain for the RAG pipeline")

            response=retrieval_chain.invoke({"input":query,
                                             "web_result":web_result})
            logger.info(f"response generated for query: {query}")
            
            return response['answer']
        except Exception as e:
            logger.error(f"error while generating for rag: {str(e)}")
            return None
        


            

            
# if __name__=="__main__":
#     input_qry = "what is happening between india and pakisthan?"
#     web_searcher = WebSearchandScraper()
#     web_res = web_searcher.web_searcher_agent(input_qry)
#     rag = RAGHandler()
#     vector_db = rag.document_loader(r"C:\Users\91623\Downloads\Generative Models.pdf")
#     response = rag.rag_generator(input_qry, vector_db, web_res)
#     logger.info(f"response got \n{response}")




