import os
from dotenv import load_dotenv


load_dotenv()
groq_api_key = os.environ.get("GROQ_API_KEY")
hf_token = os.environ.get("HUGGING_FACE_TOKEN")
chroma_db_dir = "./chroma_db"
embed_cache_dir = "./embedding_model"