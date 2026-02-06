from .base import BaseAgent

class ReviewerAgent(BaseAgent):
    def __init__(self, **kwargs):
        system_prompt = (
            "You are Kuroko Reviewer, a meticulous QA lead. "
            "Your job is to identify bugs, security vulnerabilities, and code smell. "
            "You must ensure that the implementation strictly follows the plan and project requirements."
        )
        super().__init__(name="Reviewer", role="reviewer", system_prompt=system_prompt, **kwargs)
