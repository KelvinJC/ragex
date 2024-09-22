import tempfile
from typing import List

from services.generate_response import (
    SimpleDirectoryReader, 
    VectorStoreIndex, 
    ChromaVectorStore, 
    StorageContext,
)
from services.upload_files import upload_file
from services.get_chroma import init_chroma
from exceptions.log_handler import system_logger
from exceptions.errors import FileUploadException

from utils.file_validation import check_files
from schema import Result


async def convert_files_to_embeddings(files: List, collection: str) -> Result:
    file_check = check_files(files=files)
    if file_check.get('status_code') == 200:
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                file_upload = await upload_file(files=files, temp_dir=temp_dir)
                if file_upload.is_successful:
                    embed_documents(collection=collection, dir=temp_dir)
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
    else:
        return Result(
            is_successful=False,
            error_message="File check failed",
            detail=file_check['detail'],
    ) 

def embed_documents(collection: str, dir: str) -> VectorStoreIndex:
    documents = SimpleDirectoryReader(dir).load_data()
    col = init_chroma(collection_name=collection)
    vector_store = ChromaVectorStore(chroma_collection=col)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    embeddings = VectorStoreIndex.from_documents(documents=documents, storage_context=storage_context) 
    return embeddings

    
