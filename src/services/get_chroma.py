import chromadb
from utils.config import chroma_db_dir


def init_chroma(collection_name: str, db_dir: str = chroma_db_dir) -> chromadb.Collection:
    db = chromadb.PersistentClient(path=db_dir)
    chroma_collection = db.get_or_create_collection(collection_name)
    return chroma_collection