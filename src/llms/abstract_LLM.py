'''Abstract class to be implemented by LLM's'''
from abc import ABC, abstractmethod

class AbstractLLM(ABC):
    """Abstract base class for LLM interactions."""

    @abstractmethod
    def chat_completions_create(self, messages, model: str = None):
        '''The preferred methos for other LLM's is to follow in this app the
        openAI's chat.completions.create method'''
        raise NotImplementedError("Subclasses should implement this method.")
    