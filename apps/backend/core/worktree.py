import os
import subprocess
import shutil
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class WorktreeManager:
    def __init__(self, base_repo_path: str, worktrees_dir: str):
        self.base_repo_path = os.path.abspath(base_repo_path)
        self.worktrees_dir = os.path.abspath(worktrees_dir)
        self.active_branch: Optional[str] = None
        os.makedirs(self.worktrees_dir, exist_ok=True)

    def get_active_worktree(self) -> Optional[str]:
        return self.active_branch

    def get_active_worktree_path(self) -> Optional[str]:
        if not self.active_branch:
            return None
        return os.path.join(self.worktrees_dir, self.active_branch)

    def get_active_branch(self) -> Optional[str]:
        return self.active_branch

    def create_worktree(self, branch_name: str) -> str:
        """Creates a new git worktree for a specific branch"""
        target_path = os.path.join(self.worktrees_dir, branch_name)
        
        if os.path.exists(target_path):
            logger.warning(f"Worktree path {target_path} already exists. Cleaning up...")
            self.remove_worktree(branch_name)

        try:
            # git worktree add <path> -b <branch>
            print(f"Creating worktree at {target_path} for branch {branch_name}")
            subprocess.run(
                ["git", "worktree", "add", target_path, "-b", branch_name],
                cwd=self.base_repo_path,
                check=True,
                capture_output=True,
                text=True
            )
            self.active_branch = branch_name
            return target_path
        except subprocess.CalledProcessError as e:
            logger.error(f"Error creating worktree: {e.stderr}")
            raise e

    def remove_worktree(self, branch_name: str):
        """Removes a worktree and its branch"""
        target_path = os.path.join(self.worktrees_dir, branch_name)
        
        try:
            # git worktree remove <path>
            subprocess.run(
                ["git", "worktree", "remove", "--force", target_path],
                cwd=self.base_repo_path,
                check=False,
                capture_output=True
            )
            
            # git branch -D <branch>
            subprocess.run(
                ["git", "branch", "-D", branch_name],
                cwd=self.base_repo_path,
                check=False,
                capture_output=True
            )
            
            if os.path.exists(target_path):
                shutil.rmtree(target_path)
            
            if self.active_branch == branch_name:
                self.active_branch = None
                
        except Exception as e:
            logger.error(f"Error removing worktree: {str(e)}")

    def cleanup(self):
        """Cleans up all worktrees and resets state"""
        try:
            # git worktree prune
            subprocess.run(
                ["git", "worktree", "prune"],
                cwd=self.base_repo_path,
                check=False
            )
            if self.active_branch:
                self.remove_worktree(self.active_branch)
            self.active_branch = None
        except Exception as e:
            logger.error(f"Error during worktree cleanup: {str(e)}")
