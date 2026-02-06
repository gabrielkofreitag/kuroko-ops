import pytest
import os
from unittest.mock import patch, MagicMock
from apps.backend.core.auth import get_api_key, validate_api_key

def test_get_api_key_present():
    with patch.dict(os.environ, {"OPENROUTER_API_KEY": "sk-test-key"}):
        assert get_api_key() == "sk-test-key"

def test_get_api_key_missing():
    with patch.dict(os.environ, {}, clear=True):
        if "OPENROUTER_API_KEY" in os.environ:
             del os.environ["OPENROUTER_API_KEY"]
        with pytest.raises(ValueError, match="OPENROUTER_API_KEY não definida"):
            get_api_key()

@patch("apps.backend.core.auth.OpenAI")
def test_validate_api_key_success(mock_openai):
    mock_client = mock_openai.return_value
    mock_client.models.list.return_value = MagicMock()
    
    assert validate_api_key("sk-valid-key") is True
    mock_openai.assert_called_once()

@patch("apps.backend.core.auth.OpenAI")
def test_validate_api_key_failure(mock_openai):
    mock_client = mock_openai.return_value
    mock_client.models.list.side_effect = Exception("Invalid key")
    
    assert validate_api_key("sk-invalid-key") is False
