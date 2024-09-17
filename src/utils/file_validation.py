from pathlib import Path

allowed_files = [".txt", ".csv", ".json", ".pdf", ".doc", ".docx", ".pptx"]

def is_allowed_file(filename: str):
    try:
        file_extension = Path(filename).suffix
        return file_extension.lower() in allowed_files
    except Exception as e:
        raise e

def check_files(files):
    if not files:
        return {
            "detail": "No file found", # why not a custom FileNotFoundError
            "status_code": 400,
        }
    for file in files:
        if not file or file.filename == "":
            return {
                "detail": "No selected file",
                "status_code": 400
            }        
        if not is_allowed_file(file.filename):
            print(file.filename)
            return {
                "detail": f"File format not supported. Use any of {allowed_files}",
                "status_code": 400,
            }
        
    return {
        "detail": "success",
        "status_code": 200,
    }