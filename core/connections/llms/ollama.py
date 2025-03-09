from langchain_ollama import ChatOllama
from core.interfaces import BaseLLMClient

class OllamaLLMClient(BaseLLMClient):
    """Enables connection with any model downloaded locally through Ollama software"""
    def __init__(self, model: str, **kwargs):
        self._model = ChatOllama(model=model, **kwargs)

    @property
    def model(self):
        return self._model
    
    def invoke(self, prompt, **kwargs):
        response = self.model.invoke(prompt, **kwargs)

        return response