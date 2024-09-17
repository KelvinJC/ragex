from typing import Optional
from llama_index.core import VectorStoreIndex


class Embeddings():
    state: Optional[VectorStoreIndex] = None
    
    def get_state(self):
        return self.state
    
    def set_state(cls, state: VectorStoreIndex):
        Embeddings.state = state