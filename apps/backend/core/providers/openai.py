from typing import List, Optional, Generator, AsyncGenerator
from openai import OpenAI, AsyncOpenAI
from .base import BaseProvider
from ..models import LLMMessage, LLMResponse

class OpenAIProvider(BaseProvider):
    def __init__(self, api_key: str, model: Optional[str] = None, base_url: Optional[str] = None):
        super().__init__(api_key, model, base_url)
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.async_client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self.model = model or "gpt-4o"

    def chat(self, messages: List[LLMMessage]) -> LLMResponse:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[m.model_dump() for m in messages]
        )
        return LLMResponse(
            content=response.choices[0].message.content,
            model=response.model,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        )

    async def achat(self, messages: List[LLMMessage]) -> LLMResponse:
        response = await self.async_client.chat.completions.create(
            model=self.model,
            messages=[m.model_dump() for m in messages]
        )
        return LLMResponse(
            content=response.choices[0].message.content,
            model=response.model,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        )

    def stream(self, messages: List[LLMMessage]) -> Generator[str, None, None]:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[m.model_dump() for m in messages],
            stream=True
        )
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def astream(self, messages: List[LLMMessage]) -> AsyncGenerator[str, None]:
        response = await self.async_client.chat.completions.create(
            model=self.model,
            messages=[m.model_dump() for m in messages],
            stream=True
        )
        async for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
