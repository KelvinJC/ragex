from pathlib import Path
import tempfile
from typing import List

from services.generate_response import SimpleDirectoryReader, VectorStoreIndex
from services.upload_files import upload_file
from exceptions.log_handler import system_logger
from exceptions.errors import FileUploadException

from utils.file_validation import check_files
from schema import Result


async def embed_file_and_persist(files: List, project_embeddings_dir: str):
    file_check = check_files(files=files)
    if file_check.get('status_code') == 200:
        try:
            vector_storage_path = create_storage_path('vector_db', project_embeddings_dir)
            with tempfile.TemporaryDirectory() as temp_dir:
                file_upload = await upload_file(files=files, temp_dir=temp_dir)
                if file_upload.is_successful:
                    documents = SimpleDirectoryReader(temp_dir).load_data()
                    embeddings = VectorStoreIndex.from_documents(documents=documents) 
                    embeddings.storage_context.persist(persist_dir=vector_storage_path)
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

def create_storage_path(parent_dir: str, embeddings_dir: str):
    try:
        storage_path = Path(parent_dir, embeddings_dir)
        storage_path.mkdir(exist_ok=True)
        return storage_path
    except Exception as e:
        raise e
