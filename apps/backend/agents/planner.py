from .base import BaseAgent

class PlannerAgent(BaseAgent):
    def __init__(self, **kwargs):
        system_prompt = (
            "You are Kuroko Planner, a strategic systems architect. "
            "Your role is to decompose complex user requests into clear, actionable subtasks. "
            "Output your plan in a structured markdown format with clear priorities."
        )
        super().__init__(name="Planner", role="planner", system_prompt=system_prompt, **kwargs)
