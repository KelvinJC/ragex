from typing import List

from fastapi import FastAPI, Request, UploadFile, Depends, Response
from fastapi.responses import JSONResponse, PlainTextResponse, StreamingResponse

from state import Embeddings
from services.embed import embed_file
from services.generate_response import generate

app = FastAPI()

@app.get('/health')
async def health():
    return {
        "application": "Simple LLM API",
        "message": "running successfully",
    }

@app.post('/upload')
async def process(
    files: List[UploadFile] = None, 
    urls: List[str] = None,
    session_embeddings = Depends(Embeddings),
):
    try:
        res = await embed_file(files, session_embeddings)
        if res.error_message: 
            # Use 400 STATUS CODE FOR FILE CHECK ERROR.. 
            # Perhaps a pointer to wrap all embed related func in the service
            return JSONResponse(
            content=res.detail,
            status_code=400,
        )

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
async def generate_chat(request: Request, session_embeddings: Embeddings = Depends(Embeddings)):
    req_params = await request.json()
    model = req_params["model"]
    temperature = req_params["temperature"]
    question = req_params["question"]
    try:
        response = generate(
            question=question, 
            embeddings=session_embeddings, 
            model=model, 
            temperature=temperature,
            )
        return PlainTextResponse(content=response, status_code=200)
    except Exception as e:
        return {
            "detail": "Could not generate response.",
            "status_code": 500,
        }

