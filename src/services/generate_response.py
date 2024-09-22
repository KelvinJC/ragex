from llama_index.core import (
    Settings, 
    VectorStoreIndex, 
    SimpleDirectoryReader, 
    StorageContext, 
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

from services.select_llm_client import LLMClient
from services.get_chroma import init_chroma
from exceptions.log_handler import system_logger

print("Finished llama imports...") 

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
) 

def retrieve_embeddings_index(collection: str) -> VectorStoreIndex:
    """Return the index of embeddings stored in chroma""" 
    chroma_collection = init_chroma(collection_name=collection)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection, collection_name=collection)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
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
    collection: str,
):
    try:
        init_llm_client = LLMClient(max_output_tokens=max_tokens, temperature=temperature)
        client = init_llm_client.select_client(model)
        index = retrieve_embeddings_index(collection)        
        response = query_engine( 
            query=question,
            llm_client=client,
            vector_store_index=index,
        )
        return response.response
    except Exception as e:
        system_logger.error("An error occurred during response generation.", exc_info=1)
        raise e
         