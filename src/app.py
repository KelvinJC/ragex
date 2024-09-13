from typing import List
from fastapi import FastAPI, Request, UploadFile
from services.embed import embed_file


app = FastAPI()

@app.get('/health')
async def health():
    return {
        "application": "Simple LLM API",
        "message": "running successfully",
    }

@app.post('/upload')
async def process(files: List[UploadFile] = None, urls: List[str] = None):
    try:
        res = embed_file(files, app)
        if res.error_message: 
            # Use 400 STATUS CODE FOR FILE CHECK ERROR.. 
            # Perhaps a pointer to wrap all embed related func in the service
            return {
                "detail": res.detail,
                "status_code": 400,
            }
        if res.is_successful:    
            return {
                "detail": "Embeddings generated successfully.",
                "status_code": 200,
            }
        else:
            return {
                "detail": res.detail,
                "status_code": 500,
            }  
    except Exception as e:
        return {
            "detail": "Could not generate embeddings.",
            "status_code": 500,
        }


@app.post('/generate')
async def generate_chat(request: Request):
    query = await request.json()
    pass


