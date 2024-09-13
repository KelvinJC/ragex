import tempfile
from typing import List
from services.query import SimpleDirectoryReader, VectorStoreIndex
from services.upload_files import upload_file
from exceptions.log_handler import system_logger
from exceptions.errors import FileUploadException

from schema import Result
from utils import check_file

def embed_file(files, app):
    file_check = check_file(files=files)
    if file_check['status_code'] == 200:
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                file_upload = upload_file(files=files, temp_dir=temp_dir)
                if file_upload.is_successful:
                    documents = SimpleDirectoryReader(temp_dir).load_data()
                    app.embeddings = VectorStoreIndex.from_documents(documents=documents) # store the embeddings in session... not suitable for production
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
            detail=file_upload['detail'],
    ) 