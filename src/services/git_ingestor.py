import git
import os
from src.services.memory import MemoryService
from typing import Optional
import logging

class GitIngestor:
    def __init__(self):
        self.memory_service = MemoryService()

    async def ingest_repo(self, 
                          repo_path: str, 
                          project_id: str, 
                          max_commits: int = 50):
        """
        Ingests the git history of a project into the memory layer.
        Captures: Commit messages, Author data, and changed files.
        """
        if not os.path.exists(repo_path):
            raise Exception(f"Path {repo_path} does not exist.")

        try:
            repo = git.Repo(repo_path)
            commits = list(repo.iter_commits(max_count=max_commits))
            
            for commit in commits:
                # Construct an engineering memory fact
                fact = f"Commit by {commit.author.name} on {project_id}: '{commit.message.strip()}'. "
                fact += f"Files changed: {', '.join(commit.stats.files.keys())}"
                
                await self.memory_service.add_memory(
                    raw_text=fact,
                    project_id=project_id,
                    source="git"
                )
            
            return {"status": "success", "commits_ingested": len(commits)}
            
        except Exception as e:
            logging.error(f"Failed to ingest git repo: {str(e)}")
            raise e
