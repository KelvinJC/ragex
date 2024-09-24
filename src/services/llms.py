import json
from typing import Optional

from llama_index.llms.groq import Groq
from llama_index.llms.vertex import Vertex
from anthropic import AnthropicVertex
from google.oauth2 import service_account

from utils.anthropic_base_modified import Anthropic
from utils.config import groq_api_key

class LLMService:
    def __init__(self, max_output_tokens: int = 512, temperature: float = 0.1) -> None:    
        self.groq_api_key = groq_api_key
        self.secrets_path: Optional[str] = None,
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens

    def select_client(self, model):
        model_map = {
            "llama-3.1-70b-versatile": self._groq,
            "llama-3.1-8b-instant": self._groq,
            "mixtral-8x7b-32768": self._groq,
            "claude-3-5-sonnet": self._anthropic,
            "gemini-1.5-flash": self._gemini,
            "gemini-1.5-pro": self._gemini,
        }

        _client = model_map.get(model)
        return _client(model)
    
    def _groq(self, model):
        return Groq(
            model, 
            api_key=self.groq_api_key, 
            temperature=self.temperature,
            max_tokens=self.max_output_tokens,
        )
    
    def _gemini(self, model):
        credentials = self._load_credentials()
        return Vertex(
            model=model,
            project_id=credentials.project_id,
            credentials=credentials,
            max_tokens=self.max_output_tokens,
        )
    
    def _anthropic(self, model):
        credentials = self._load_credentials()
        region_map = {
            "claude-3-5-sonnet": "us-east5",
            "claude-3-haiku": "us-central1",
        }
        vertex_client = AnthropicVertex(
            project_id=credentials.project_id,
            region=region_map.get(model),
        )
        return Anthropic(
            model=model,
            vertex_client=vertex_client,
            max_tokens=self.max_output_tokens,
        )

    def _load_credentials(self):
        with open(self.secrets_path, "r") as file:
            secrets = json.loads(file)
        
        credentials = (
            service_account
            .Credentials
            .from_service_account_info(
                secrets,
                scopes=["https://www.googleapis.com/auth/cloud-platform.read-only"],
            )
        )
        return credentials
