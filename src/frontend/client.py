from typing import Dict, List, Tuple

import requests


def post_request_to_api(
    url: str, 
    question: str, 
    model: str, 
    temperature: float, 
    max_tokens: int, 
    project_id: str
):
    """Send the user input to backend API"""
    response = requests.post(
        url,
        json={
            "question": question,
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "project_id": project_id,
        },
        stream=True,
    )
    return response

def configure_file_payload(file) -> Tuple:
    return ("files", (file.name, file.read(), "application/pdf"))

def upload_files_to_api(url: str, payload: Dict, files: List):
    """Upload files to backend API"""
    all_file_content = [configure_file_payload(file) for file in files]
    response = requests.post(url, data=payload, files=all_file_content) # stream=True,
    return response
