from typing import List

from fastapi import FastAPI, HTTPException, Request, UploadFile, Depends, Response
from fastapi.responses import JSONResponse, PlainTextResponse, StreamingResponse

from state import Embeddings
from services.embed import embed_file
from services.generate_response import generate
from exceptions.log_handler import system_logger

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
            raise HTTPException(status_code=400, detail=res.detail)

        if res.is_successful:    
            return {
                "detail": "Embeddings generated successfully.",
                "status_code": 200,
            }
        else:
            raise HTTPException(status_code=500, detail=res.detail)
        
    except HTTPException as e:
        system_logger.error(f"Error: {str(e)}")
        raise e
    except Exception as e:
        system_logger.error(f"Error generating embeddings: {e}")
        raise HTTPException(status_code=500, detail="Could not generate embeddings.")


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

