import logging
import json
import re
from typing import List, Dict, Any, Optional
from ..core.async_llm_client import AsyncLLMClient
from ..core.models import LLMMessage, LLMResponse
from ..core.tools.registry import registry as tool_registry

logger = logging.getLogger(__name__)

from ..core.utils.tokens import truncate_messages

class BaseAgent:
    def __init__(
        self, 
        name: str, 
        role: str, 
        system_prompt: str,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        max_context_tokens: int = 128000
    ):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt + "\n\nAvailable tools:\n- read_file(path)\n- write_file(path, content)\n- run_command(command)\n\nTo use a tool, output: <tool_call name=\"tool_name\">{\"arg\": \"value\"}</tool_call>"
        self.client = AsyncLLMClient(api_key=api_key, model=model, base_url=base_url)
        self.max_context_tokens = max_context_tokens
        self.messages: List[LLMMessage] = [
            LLMMessage(role="system", content=self.system_prompt)
        ]

    async def run(self, user_input: str, max_iterations: int = 5) -> str:
        """Main execution loop for the agent with tool calling support"""
        self.messages.append(LLMMessage(role="user", content=user_input))
        
        for i in range(max_iterations):
            logger.info(f"Agent {self.name} iteration {i+1}")
            
            # Context Management: Sliding window
            active_messages = truncate_messages(self.messages, self.max_context_tokens, self.client.model)
            
            response = await self.client.chat(active_messages)
            content = response.content
            self.messages.append(LLMMessage(role="assistant", content=content))
            
            # Check for tool calls
            tool_call_match = re.search(r'<tool_call name="(.+?)">(.+?)</tool_call>', content, re.DOTALL)
            if not tool_call_match:
                return content # Final response
                
            tool_name = tool_call_match.group(1)
            tool_args_str = tool_call_match.group(2)
            
            try:
                tool_args = json.loads(tool_args_str)
                print(f"[{self.name}] Calling tool {tool_name} with {tool_args}")
                result = tool_registry.execute_tool(tool_name, tool_args)
                self.messages.append(LLMMessage(role="user", content=f"Tool result: {result}"))
            except Exception as e:
                self.messages.append(LLMMessage(role="user", content=f"Error parsing tool args: {str(e)}"))
        
        return "Max iterations reached without a final response."

    def clear_history(self):
        self.messages = [LLMMessage(role="system", content=self.system_prompt)]

class CoderAgent(BaseAgent):
    def __init__(self, **kwargs):
        system_prompt = (
            "You are Kuroko Coder, an expert software engineer. "
            "Your goal is to implement features based on a specification. "
            "Use tools to read existing code and write your implementation."
        )
        super().__init__(name="Coder", role="coder", system_prompt=system_prompt, **kwargs)

class ReviewerAgent(BaseAgent):
    def __init__(self, **kwargs):
        system_prompt = (
            "You are Kuroko Reviewer, a meticulous senior engineer. "
            "Review code by using read_file to examine the implementations."
        )
        super().__init__(name="Reviewer", role="reviewer", system_prompt=system_prompt, **kwargs)
