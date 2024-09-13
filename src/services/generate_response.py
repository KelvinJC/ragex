from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings #, ServiceContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from services.clients import LLMClient
from state import Embeddings
from exceptions.log_handler import system_logger

print("Finished llama imports...") 

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)


def query_engine(query: str, vector_store_index: VectorStoreIndex, llm_client):
    query_engine = vector_store_index.as_query_engine(llm=llm_client, similarity_top_k=10)
    response = query_engine.query(query)
    return response

def generate(question: str, embeddings: Embeddings, model: str, temperature: float):
    try:
        init_llm_client = LLMClient(temperature=temperature)
        client = init_llm_client.select_client(model)
        response = query_engine( 
            query=question,
            vector_store_index=embeddings.get_state(),
            llm_client=client,
        )
        return response.response
    except Exception as e:
        system_logger.error("An error occurred during response generation.", exc_info=1)
        raise e
        