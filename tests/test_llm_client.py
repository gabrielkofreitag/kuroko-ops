import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from apps.backend.core.llm_client import LLMClient
from apps.backend.core.async_llm_client import AsyncLLMClient
from apps.backend.core.models import LLMResponse

def test_llm_client_initialization():
    with patch.dict("os.environ", {"OPENROUTER_API_KEY": "test-key", "DEFAULT_MODEL": "test-model"}):
        client = LLMClient()
        assert client.api_key == "test-key"
        assert client.model == "test-model"

def test_llm_client_chat():
    with patch("apps.backend.core.llm_client.OpenAI") as mock_openai:
        mock_client = mock_openai.return_value
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Hello!"))]
        mock_response.model = "test-model"
        mock_response.usage = MagicMock(prompt_tokens=10, completion_tokens=5, total_tokens=15)
        mock_client.chat.completions.create.return_value = mock_response

        client = LLMClient(model="test-model")
        response = client.chat([{"role": "user", "content": "Hi"}])

        assert isinstance(response, LLMResponse)
        assert response.content == "Hello!"
        assert response.usage.total_tokens == 15

@pytest.mark.asyncio
async def test_async_llm_client_chat():
    with patch("apps.backend.core.async_llm_client.AsyncOpenAI") as mock_async_openai:
        mock_client = mock_async_openai.return_value
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Hello Async!"))]
        mock_response.model = "test-model"
        mock_response.usage = MagicMock(prompt_tokens=10, completion_tokens=5, total_tokens=15)
        
        # Use AsyncMock for the create call
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        client = AsyncLLMClient(model="test-model")
        response = await client.chat([{"role": "user", "content": "Hi"}])

        assert isinstance(response, LLMResponse)
        assert response.content == "Hello Async!"
