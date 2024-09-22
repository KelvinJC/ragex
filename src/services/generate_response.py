from typing import Tuple
from llama_index.core import (
    Settings, 
    VectorStoreIndex, 
    SimpleDirectoryReader, 
    StorageContext, 
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

from services.select_llm_client import LLMService
from services.get_chroma import init_chroma, get_knowledge_base_size
from exceptions.log_handler import system_logger

print("Finished llama imports...") 

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
) 

def generate(question: str, model: str, temperature: float, max_tokens: int, collection: str):
    try:
        llm = LLMService(max_output_tokens=max_tokens, temperature=temperature)
        client = llm.select_client(model)
        index, col_size = retrieve_embeddings_index_and_size(collection) 
        top_k = get_choice_k(col_size)       
        response = query_engine( 
            query=question,
            llm_client=client,
            vector_store_index=index,
            choice_k=top_k,
        )
        return response.response
    except Exception as e:
        system_logger.error("An error occurred during response generation.", exc_info=1)
        raise e

def retrieve_embeddings_index_and_size(collection: str) -> Tuple[VectorStoreIndex, int]:
    """Return a tuple with the index of embeddings stored in chroma and their size""" 
    chroma_collection = init_chroma(collection_name=collection)
    retrieved_col_size = get_knowledge_base_size(collection=chroma_collection)
    print(f"Retrieved collection size: {retrieved_col_size}")
    # TODO: Set up embeddings logger to track embedding sizes
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection, collection_name=collection)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    return index, retrieved_col_size

def get_choice_k(collection_size: int) -> int:
    try:
        int(collection_size)
    except ValueError as e:
        raise e
    
    if collection_size > 150:
        return 40
    elif collection_size > 50:
        return 15
    elif collection_size > 10:
        return 5
    else:
        return collection_size

def query_engine(query: str, vector_store_index: VectorStoreIndex, llm_client: LLMService, choice_k: int):
    query_engine = vector_store_index.as_query_engine(llm=llm_client, similarity_top_k=choice_k)
    response = query_engine.query(query)
    return response

         