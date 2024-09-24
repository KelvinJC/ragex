from typing import List

from fastapi import FastAPI, Form, HTTPException, Request, UploadFile
from fastapi.responses import PlainTextResponse, StreamingResponse

from services.generate_embeddings import convert_files_to_embeddings
from services.generate_response import generate
from services.get_chroma import get_knowledge_base_size, init_chroma
from services.chat_response_engine import ChatEngine
from exceptions.log_handler import system_logger

app = FastAPI()

@app.get('/health')
async def health():
    return {
        "application": "LLM RAG System API",
        "message": "running successfully",
    }


@app.post('/upload')
async def process(
    project_id: str = Form(...),
    files: List[UploadFile] = None, 
    # urls: List[str] = None,
):
    try:
        res = await convert_files_to_embeddings(files, collection=project_id)
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
async def generate_chat(request: Request):
    req_params = await request.json()
    model = req_params["model"]
    temperature = req_params["temperature"]
    question = req_params["question"]
    max_tokens = req_params["max_tokens"]
    project_id = req_params["project_id"]
    # modify top k from req_params

    chat_engine = ChatEngine()
    app.state.chat_memory = chat_engine.retrieve_chat_memory(memory_source=app.state)
    chat_memory = app.state.chat_memory
    try:
        response = chat_engine.stream_chat_response(
            question=question,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            collection=project_id,
            llm_memory=chat_memory,
        )
        return StreamingResponse(content=response, status_code=200, media_type="text/event-stream") # use this option for production
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not generate response. {str(e)}")

