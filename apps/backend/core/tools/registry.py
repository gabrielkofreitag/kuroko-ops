import os
import subprocess
from typing import Dict, Any, Callable

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Callable] = {}

    def register_tool(self, name: str, func: Callable):
        self.tools[name] = func

    def execute_tool(self, name: str, args: Dict[str, Any]) -> Any:
        if name not in self.tools:
            return f"Error: Tool {name} not found."
        try:
            return self.tools[name](**args)
        except Exception as e:
            return f"Error executing {name}: {str(e)}"

# Define built-in tools
def read_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path: str, content: str) -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return f"File written to {path}"

def run_command(command: str) -> str:
    # Security: In a real app, we'd check for dangerous patterns
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else result.stderr

from core.memory import MemoryService, init_memory_db
from core.database import SessionLocal

# Initialize memory
init_memory_db()

def store_memory(category: str, content: str) -> str:
    db = SessionLocal()
    try:
        service = MemoryService(db)
        service.add_memory(category, content)
        return f"Memory stored in category '{category}'"
    finally:
        db.close()

def search_memory(query: str) -> str:
    db = SessionLocal()
    try:
        service = MemoryService(db)
        return service.search_memory(query)
    finally:
        db.close()

# Global registry
registry = ToolRegistry()
registry.register_tool("read_file", read_file)
registry.register_tool("write_file", write_file)
registry.register_tool("run_command", run_command)
registry.register_tool("git_commit", git_commit)
registry.register_tool("git_push", git_push)
registry.register_tool("create_workspace", create_workspace)
registry.register_tool("store_memory", store_memory)
registry.register_tool("search_memory", search_memory)
