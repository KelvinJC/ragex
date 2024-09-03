from typing import List
from fastapi import FastAPI, Request, UploadFile
from chat import *

app = FastAPI()

@app.get('/health')
async def health():
    return {
        "application": "Simple LLM API",
        "message": "running successfully"
    }

@app.post('/upload')
async def process(
    files: List[UploadFile] = None,
    urls: List[str] = None,
):
    
    if files:
        pass
        

@app.post('/generate')
async def generate_chat(request: Request):
    query = await request.json()
    pass
