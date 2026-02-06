from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ChatMessage(BaseModel):
    role: str
    content: str
    name: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None

class LLMUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

class LLMResponse(BaseModel):
    content: str
    model: str
    usage: Optional[LLMUsage] = None
    cost: Optional[float] = None

class AgentConfig(BaseModel):
    name: str
    model: str
    system_prompt: str
    max_tokens: int = 4096
    temperature: float = 0.0
