from pathlib import Path
from typing import List
import tempfile

from fastapi import UploadFile
from werkzeug.utils import secure_filename

from services.generation import (
    SimpleDirectoryReader, 
    VectorStoreIndex, 
    ChromaVectorStore, 
    StorageContext,
)
from services.chroma_db import init_chroma, get_knowledge_base_size
from schema import Result
from exceptions.log_handler import system_logger
from exceptions.errors import FileUploadException
    
    
async def process_files_for_embeddings(files: List, collection: str) -> Result:
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_upload = await upload_file(files=files, temp_dir=temp_dir)
            if file_upload.is_successful:
                create_embeddings(collection=collection, dir=temp_dir)
                return Result(
                    is_successful=True,
                    detail="Embeddings generated successfully.",
                )  
    except FileUploadException:
        system_logger.error("An error occurred during file upload.", exc_info=1)
        return Result(
            is_successful=False,
            detail="File Upload Error.",
        )        
    except Exception as e:
        system_logger.error("An error occurred during embedding.", exc_info=1)
        return Result(
            is_successful=False,
            detail="Could not generate embeddings.",
        )

async def upload_file(files: List[UploadFile], temp_dir: str) -> Result:
    try:
        for file in files:
            filename = secure_filename(file.filename)
            file_path = Path(temp_dir, filename)
            file_object = await file.read()
            with open(file_path, "wb") as buffer:
                buffer.write(file_object)
        return Result(
            is_successful=True,
            detail="Files uploaded successfully.",
        )
    except Exception as e:
        message = f"An error occurred during upload."
        system_logger.error(
            message,
            exc_info=1
        )
        raise FileUploadException(message)

def create_embeddings(collection: str, dir: str) -> VectorStoreIndex:
    documents = SimpleDirectoryReader(dir).load_data()
    col = init_chroma(collection_name=collection)
    col_size_before_embedding = get_knowledge_base_size(collection=col)
    
    vector_store = ChromaVectorStore(chroma_collection=col)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    embeddings = VectorStoreIndex.from_documents(documents=documents, storage_context=storage_context) 
    
    col_size_after_embedding = get_knowledge_base_size(collection=col)
    # TODO: Replace with new diff logger
    system_logger.info(f"Embedding size is {col_size_after_embedding - col_size_before_embedding}")
    print(f"Size of generated embeddings is {col_size_after_embedding - col_size_before_embedding}")
    return embeddings

    
