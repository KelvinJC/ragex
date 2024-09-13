from llama_index.llms.groq import Groq
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings #, ServiceContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from config import groq_api_key

print("Finished llama imports...") 

models = [
    # "llama-3.1-405b-reasoning",
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "claude-3-5-sonnet",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
]

""" 
Two ways to set llm and embed models can be set at any of 2 levels
    - global setting with Settings (both llm and embed model)
    - index level (embed model only)
    - query engine level (llm only)
"""

# Settings.embed_model
# Settings.llm

# if you want global settings
# Settings.embed_model = HuggingFaceEmbedding(
#     model_name="BAAI/bge-small-en-v1.5"
# )

# Settings.llm = Groq(
#     model = "",
#     api_key=groq_api_key,
#     temperature=0.1,
# )


Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

# llm = Groq(
#     model = "",
#     api_key=groq_api_key,
#     temperature=0.1,
# )

def upload_doc(dir):
    documents = SimpleDirectoryReader(dir).load_data()
    index = VectorStoreIndex.from_documents(documents) # embed_model is set globally so no need to pass in arg
    return index

def query_engine(query: str, index: VectorStoreIndex, model=models[0]):
    llm = Groq(
        model = model,
        api_key=groq_api_key,
        temperature=0.1,
    )
    query_engine = index.as_query_engine(llm=llm, similarity_top_k=10)
    response = query_engine.query(query)
    return response

if __name__ == "__main__":
    index = upload_doc("./text")
    continue_qa = None
    while continue_qa != "n":
        query = input("Ask me anything: ")
        model = input("Enter model code: ")

        response = query_engine(query=query, index=index, model=model)
        print("Response: ", response)
        continue_qa = input("Continue ? ")
    