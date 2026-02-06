from .base import BaseAgent

class CoderAgent(BaseAgent):
    def __init__(self, **kwargs):
        system_prompt = (
            "You are Kuroko Coder, a world-class senior software engineer. "
            "You specialize in writing clean, efficient, and well-documented code. "
            "You always follow architectural patterns and prioritize security and performance."
        )
        super().__init__(name="Coder", role="coder", system_prompt=system_prompt, **kwargs)
