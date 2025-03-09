from abc import ABC, abstractmethod

class BaseLLMClient(ABC):
    """Interface for communication with LLM models"""

    @property
    @abstractmethod
    def model(self):
        """LLM model instance"""
        pass

    @abstractmethod
    def run(self, prompt: str, **kwargs) -> str:
        """Generates an answer based on a prompt"""
        pass