from typing import List

from fastapi import FastAPI, Form, HTTPException, Request, UploadFile
from fastapi.responses import StreamingResponse

from services.retrieval import process_files_for_embeddings
from services.generation import ChatEngine
from exceptions.log_handler import system_logger, user_ops_logger
from utils.file_validation import check_files


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
        file_check = check_files(files)
        if file_check.get('status_code') != 200:
            system_logger.error(file_check.get('detail'))
            raise HTTPException(status_code=400, detail=file_check.get('detail'))            

        res = await process_files_for_embeddings(files, collection=project_id)
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
    model = req_params.get("model")
    temperature = req_params.get("temperature")
    question = req_params.get("question")
    max_tokens = req_params.get("max_tokens")
    project_id = req_params.get("project_id")
    # modify top k from req_params

    chat_engine = ChatEngine()
    app.state.chat_memory = chat_engine.retrieve_chat_memory(memory_source=app.state)
    chat_memory = app.state.chat_memory
    try:
        response = chat_engine.generate_response(
            question=question,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            collection=project_id,
            llm_memory=chat_memory,
        )
        return StreamingResponse(content=response, status_code=200, media_type="text/event-stream")
    except Exception as e:
        user_ops_logger.error(f"Error generating a respone {e}", exc_info=1)
        raise HTTPException(status_code=500, detail=f"Could not generate response. {str(e)}")

