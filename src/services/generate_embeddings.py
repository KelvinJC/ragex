from pathlib import Path
import tempfile

from services.generate_response import SimpleDirectoryReader, VectorStoreIndex
from services.upload_files import upload_file
from exceptions.log_handler import system_logger
from exceptions.errors import FileUploadException

from utils.file_validation import check_files
from schema import Result
from state import Embeddings


async def embed_file(files, session_embeddings: Embeddings):
    file_check = check_files(files=files)
    if file_check.get('status_code') == 200:
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                file_upload = await upload_file(files=files, temp_dir=temp_dir)
                if file_upload.is_successful:
                    documents = SimpleDirectoryReader(temp_dir).load_data()
                    embeddings = VectorStoreIndex.from_documents(documents=documents) 
                    session_embeddings.set_state(embeddings) # store the embeddings in session... not suitable for production
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

async def embed_file_and_persist(files):
    file_check = check_files(files=files)
    if file_check.get('status_code') == 200:
        try:
            vector_storage_path = Path('vector_db')
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