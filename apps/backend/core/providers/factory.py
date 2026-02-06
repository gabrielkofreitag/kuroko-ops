from typing import Optional
from .base import BaseProvider
from .openai import OpenAIProvider
from .openrouter import OpenRouterProvider

class ProviderFactory:
    @staticmethod
    def get_provider(
        api_key: str, 
        model: Optional[str] = None, 
        base_url: Optional[str] = None
    ) -> BaseProvider:
        # Simple heuristic to determine provider
        # If model contains '/', it's likely OpenRouter (e.g., 'anthropic/claude-3')
        # unless it's a specific OpenAI local deployment
        
        if base_url and "openrouter.ai" in base_url:
            return OpenRouterProvider(api_key, model, base_url)
        
        if model and "/" in model:
            # Check if it's a known OpenRouter-style model
            return OpenRouterProvider(api_key, model, base_url)
            
        # Default fallback to OpenAI (which works for most compatible APIs)
        return OpenAIProvider(api_key, model, base_url)
