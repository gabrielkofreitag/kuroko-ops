import os
from typing import List, Optional, Generator
from .providers.factory import ProviderFactory
from .models import LLMMessage, LLMResponse

class LLMClient:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None, base_url: Optional[str] = None):
        api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.provider = ProviderFactory.get_provider(api_key, model, base_url)

    def chat(self, messages: List[LLMMessage]) -> LLMResponse:
        return self.provider.chat(messages)

    def chat_stream(self, messages: List[LLMMessage]) -> Generator[str, None, None]:
        return self.provider.stream(messages)

    @property
    def api_key(self):
        return self.provider.api_key

    @property
    def model(self):
        return self.provider.model
