from pathlib import Path
from llama_index.core import (
    VectorStoreIndex, 
    SimpleDirectoryReader, 
    Settings, 
    StorageContext, 
    load_index_from_storage,
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from services.select_llm_client import LLMClient
from exceptions.log_handler import system_logger

print("Finished llama imports...") 

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

def get_embeddings_index(project_dir):
    """Return the index of stored embeddings""" 
    storage_path = Path("vector_db", project_dir)
    storage_context = StorageContext.from_defaults(persist_dir=storage_path) 
    index = load_index_from_storage(storage_context)
    return index

def query_engine(query: str, vector_store_index: VectorStoreIndex, llm_client: LLMClient):
    query_engine = vector_store_index.as_query_engine(llm=llm_client, similarity_top_k=10)
    response = query_engine.query(query)
    return response

def generate(
    question: str, 
    model: str, 
    temperature: float, 
    max_tokens: int, 
    project_embeddings_dir: str,
):
    try:
        init_llm_client = LLMClient(max_output_tokens=max_tokens, temperature=temperature)
        client = init_llm_client.select_client(model)
        index = get_embeddings_index(project_embeddings_dir)        
        response = query_engine( 
            query=question,
            llm_client=client,
            vector_store_index=index,
        )
        return response.response
    except Exception as e:
        system_logger.error("An error occurred during response generation.", exc_info=1)
        raise e
         