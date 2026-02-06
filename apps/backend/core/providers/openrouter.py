from .openai import OpenAIProvider

class OpenRouterProvider(OpenAIProvider):
    def __init__(self, api_key: str, model: Optional[str] = None, base_url: Optional[str] = None):
        # Default OpenRouter base URL if not provided
        base_url = base_url or "https://openrouter.ai/api/v1"
        model = model or "anthropic/claude-3.5-sonnet"
        super().__init__(api_key, model, base_url)
