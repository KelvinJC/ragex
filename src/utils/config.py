import os
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.environ.get("GROQ_API_KEY")
vector_store_dir = "vector_db"
chroma_db_dir = "./chroma_db"