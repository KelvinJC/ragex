from pathlib import Path
from typing import List
from fastapi import UploadFile
from werkzeug.utils import secure_filename
from exceptions.log_handler import system_logger
from exceptions.errors import FileUploadException
from schema import Result


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
