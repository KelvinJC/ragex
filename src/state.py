from typing import Optional
from services.generate_response import VectorStoreIndex


class Embeddings():
    state: Optional[VectorStoreIndex] = None
    
    def get_state(self):
        return self.state
    
    def set_state(self, state: VectorStoreIndex):
        Embeddings.state = state