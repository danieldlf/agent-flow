from core.interfaces import BaseLLMClient
from core.connections.llms import OllamaLLMClient

class LLMService():
    """Service responsible to provide the correct model given the context"""
    
    @staticmethod
    def get_model(provider: str, **kwargs) -> BaseLLMClient:
        """Get the correct service for the chosen model/provider"""
        if provider == "ollama":
            return OllamaLLMClient(**kwargs).model
        
        # Add other providers
        
        else:
            raise ValueError(f"Provedor: '{provider}' não suportado.")
