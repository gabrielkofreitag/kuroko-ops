import logging
import asyncio
from typing import List, Dict, Any, Optional
from .planner import PlannerAgent
from .coder import CoderAgent
from .qa_reviewer import ReviewerAgent

logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self, websocket: Optional[Any] = None, **llm_kwargs):
        self.websocket = websocket
        self.llm_kwargs = llm_kwargs
        self.planner = PlannerAgent(**llm_kwargs)
        self.coder = CoderAgent(**llm_kwargs)
        self.reviewer = ReviewerAgent(**llm_kwargs)

    async def _emit_thought(self, agent: str, content: str):
        if self.websocket:
            await self.websocket.send_json({
                "type": "thought",
                "agent": agent,
                "content": content
            })

    async def execute_task(self, task_description: str):
        """Orchestrate the planning, coding, and review cycle"""
        logger.info(f"Starting orchestration for task: {task_description[:50]}...")

        # 1. Planning
        await self._emit_thought("Planner", "Decomposing task into subtasks...")
        plan = await self.planner.run(f"Create a plan for: {task_description}")
        await self._emit_thought("Planner", f"Plan generated:\n{plan}")
        
        # 2. Coding
        await self._emit_thought("Coder", "Implementing plan...")
        implementation = await self.coder.run(f"Follow this plan: {plan}\n\nTask: {task_description}")
        await self._emit_thought("Coder", "Implementation complete.")
        
        # 3. Review
        await self._emit_thought("Reviewer", "Starting code review...")
        review = await self.reviewer.run(f"Review this implementation:\n\n{implementation}")
        await self._emit_thought("Reviewer", f"Review results: {review}")
        
        return {
            "plan": plan,
            "implementation": implementation,
            "review": review
        }
