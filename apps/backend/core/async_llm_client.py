import os
from typing import List, Optional, AsyncGenerator
from .providers.factory import ProviderFactory
from .models import LLMMessage, LLMResponse

class AsyncLLMClient:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None, base_url: Optional[str] = None):
        api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.provider = ProviderFactory.get_provider(api_key, model, base_url)

    async def chat(self, messages: List[LLMMessage]) -> LLMResponse:
        return await self.provider.achat(messages)

    def chat_stream(self, messages: List[LLMMessage]) -> AsyncGenerator[str, None]:
        return self.provider.astream(messages)

    @property
    def api_key(self):
        return self.provider.api_key

    @property
    def model(self):
        return self.provider.model
