from abc import ABC, abstractmethod

class AbstractLLM(ABC):
    """Abstract base class for LLM interactions."""

    @abstractmethod
    def chat_completions_create(self, messages, model: str = None):
        raise NotImplementedError("Subclasses should implement this method.")
    