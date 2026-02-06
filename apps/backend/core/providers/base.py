from abc import ABC, abstractmethod
from typing import List, Optional, Generator, AsyncGenerator
from ..models import LLMMessage, LLMResponse

class BaseProvider(ABC):
    def __init__(self, api_key: str, model: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url

    @abstractmethod
    def chat(self, messages: List[LLMMessage]) -> LLMResponse:
        """Synchronous chat completion"""
        pass

    @abstractmethod
    async def achat(self, messages: List[LLMMessage]) -> LLMResponse:
        """Asynchronous chat completion"""
        pass

    @abstractmethod
    def stream(self, messages: List[LLMMessage]) -> Generator[str, None, None]:
        """Synchronous streaming"""
        pass

    @abstractmethod
    def astream(self, messages: List[LLMMessage]) -> AsyncGenerator[str, None]:
        """Asynchronous streaming"""
        pass
