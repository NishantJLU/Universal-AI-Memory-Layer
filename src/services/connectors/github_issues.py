import requests
import os
from src.services.memory import MemoryService
import logging

class GitHubIssuesConnector:
    def __init__(self):
        self.memory_service = MemoryService()
        self.token = os.getenv("GITHUB_TOKEN")

    async def ingest_issues(self, repo_owner: str, repo_name: str, project_id: str):
        """
        Fetches open issues from a GitHub repo and ingests them as memories.
        """
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
        headers = {"Authorization": f"token {self.token}"} if self.token else {}
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch issues: {response.text}")
            
        issues = response.json()
        count = 0
        for issue in issues:
            # Skip pull requests (which are also returned by the issues API)
            if "pull_request" in issue:
                continue
                
            fact = f"GitHub Issue #{issue['number']} ({issue['title']}): {issue['body'][:500]}"
            await self.memory_service.add_memory(
                raw_text=fact,
                project_id=project_id,
                source="github_issues"
            )
            count += 1
            
        return {"status": "success", "issues_ingested": count}
