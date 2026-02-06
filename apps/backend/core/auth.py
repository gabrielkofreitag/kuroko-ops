import os
from typing import Optional
from openai import OpenAI

def get_api_key() -> str:
    """
    Recupera a API Key do OpenRouter das variáveis de ambiente.
    """
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        raise ValueError(
            "OPENROUTER_API_KEY não definida. "
            "Copie .env.example → .env e preencha."
        )
    return key

def validate_api_key(key: str) -> bool:
    """
    Testa a key fazendo um request mínimo ao OpenRouter (listagem de modelos).
    """
    try:
        client = OpenAI(
            api_key=key,
            base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        )
        # Tenta listar modelos para validar a chave
        client.models.list()
        return True
    except Exception as e:
        print(f"Erro na validação da API Key: {e}")
        return False
