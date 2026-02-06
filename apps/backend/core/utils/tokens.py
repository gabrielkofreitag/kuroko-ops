import tiktoken
from typing import List, Dict, Any
from ..models import LLMMessage

def count_tokens(messages: List[LLMMessage], model: str = "gpt-4o") -> int:
    """
    Counts tokens for a list of messages.
    Note: Token counting varies by provider, this is an approximation using tiktoken for OpenAI models.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # Fallback to cl100k_base for newer/unknown models
        encoding = tiktoken.get_encoding("cl100k_base")

    num_tokens = 0
    for message in messages:
        # Every message follows <im_start>{role/name}\n{content}<im_end>\n
        num_tokens += 4 
        num_tokens += len(encoding.encode(message.role))
        num_tokens += len(encoding.encode(message.content))
        
    num_tokens += 2  # Every reply is primed with <im_start>assistant
    return num_tokens

def truncate_messages(messages: List[LLMMessage], max_tokens: int, model: str = "gpt-4o") -> List[LLMMessage]:
    """
    Truncates a list of messages to fit within a token limit using a sliding window.
    Always preserves the system message.
    """
    if not messages:
        return []

    system_msg = messages[0] if messages[0].role == "system" else None
    
    current_messages = messages.copy()
    while count_tokens(current_messages, model) > max_tokens and len(current_messages) > (2 if system_msg else 1):
        # Remove the oldest message (after system message)
        if system_msg:
            current_messages.pop(1)
        else:
            current_messages.pop(0)
            
    return current_messages
