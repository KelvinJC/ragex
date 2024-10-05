import chromadb
from utils.config import chroma_db_dir


def init_chroma(collection_name: str, db_dir: str = chroma_db_dir) -> chromadb.Collection:
    """
    Get or create a collection with the given collection name.
    Args:
        collection_name: The name of the collection to be retrieved or created.
        db_dir: The directory to save Chroma's data to.
    Returns:
        The collection.
    """
    db = chromadb.PersistentClient(path=db_dir)
    chroma_collection = db.get_or_create_collection(collection_name)
    return chroma_collection


def get_knowledge_base_size(collection: chromadb.Collection) -> int:
    """
    Returns the number of embeddings in a specified collection.
    Args:
        collection: The collection to count the embeddings in.
    Returns:
        int: The number of embeddings in the collection
    """
    return collection.count()

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