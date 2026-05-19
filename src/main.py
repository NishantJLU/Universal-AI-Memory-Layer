from fastapi import FastAPI, Depends, HTTPException, Request, Header
from sqlmodel import Session, create_engine, select
from src.models.memory import Memory
from src.services.memory import MemoryService
from src.services.search import SearchService
from src.services.git_ingestor import GitIngestor
from src.services.conflict_resolver import ConflictResolver
from src.services.connectors.github_issues import GitHubIssuesConnector
from src.services.ast_ingestor import ASTIngestor
from pydantic import BaseModel
from typing import Optional, List
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/universal_ai_layer")
engine = create_engine(DATABASE_URL)

app = FastAPI(title="Universal AI Layer")

# v3.0: Basic Auth
API_KEY = os.getenv("UNIVERSAL_API_KEY", "dev_key")

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

memory_service = MemoryService()
search_service = SearchService()
git_ingestor = GitIngestor()
conflict_resolver = ConflictResolver()
github_connector = GitHubIssuesConnector()
ast_ingestor = ASTIngestor()

class MemoryCreate(BaseModel):
    text: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    project_id: Optional[str] = None
    source: Optional[str] = "user"

class GitIngestRequest(BaseModel):
    repo_path: str
    project_id: str
    max_commits: Optional[int] = 50

class GitHubIngestRequest(BaseModel):
    owner: str
    repo: str
    project_id: str

class ASTIngestRequest(BaseModel):
    path: str
    project_id: str

class ValidationRequest(BaseModel):
    memory_id: int
    approved: bool

@app.post("/add", dependencies=[Depends(verify_api_key)])
async def add_memory(item: MemoryCreate):
    try:
        await memory_service.add_memory(
            raw_text=item.text,
            user_id=item.user_id,
            session_id=item.session_id,
            project_id=item.project_id,
            source=item.source
        )
        return {"status": "success", "message": "Memory processed and stored."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search", dependencies=[Depends(verify_api_key)])
async def search_memory(query: str, project_id: Optional[str] = None, limit: Optional[int] = 5):
    try:
        return await search_service.hybrid_search(query, project_id, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest/git", dependencies=[Depends(verify_api_key)])
async def ingest_git(item: GitIngestRequest):
    try:
        return await git_ingestor.ingest_repo(item.repo_path, item.project_id, item.max_commits)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest/github-issues", dependencies=[Depends(verify_api_key)])
async def ingest_github_issues(item: GitHubIngestRequest):
    try:
        return await github_connector.ingest_issues(item.owner, item.repo, item.project_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest/ast", dependencies=[Depends(verify_api_key)])
async def ingest_ast(item: ASTIngestRequest):
    try:
        ast_ingestor.ingest_directory(item.path, item.project_id)
        return {"status": "success", "message": "AST ingestion complete."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/webhooks/{provider}", dependencies=[Depends(verify_api_key)])
async def handle_webhook(provider: str, request: Request, project_id: str):
    try:
        data = await request.json()
        fact = f"Webhook event from {provider}: {str(data)[:1000]}"
        await memory_service.add_memory(raw_text=fact, project_id=project_id, source=f"webhook_{provider}")
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/validate", dependencies=[Depends(verify_api_key)])
async def validate_memory(item: ValidationRequest):
    try:
        with Session(engine) as session:
            memory = session.get(Memory, item.memory_id)
            if not memory:
                raise HTTPException(status_code=404, detail="Memory not found")
            memory.is_validated = item.approved
            session.commit()
            return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/audit", dependencies=[Depends(verify_api_key)])
async def audit_project(project_id: str):
    try:
        conflicts = await conflict_resolver.audit_memories(project_id)
        return {"status": "success", "conflicts_found": len(conflicts), "conflicts": conflicts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/onboard/{project_id}", dependencies=[Depends(verify_api_key)])
async def generate_onboarding_brief(project_id: str):
    try:
        with Session(engine) as session:
            summaries = session.exec(
                select(Memory)
                .where(Memory.project_id == project_id, Memory.is_summary == True)
                .order_by(Memory.importance_score.desc())
            ).all()
            
            if not summaries:
                return {"brief": "No project summary available yet. Please ingest some data first."}
            
            brief = f"# Onboarding Brief for Project: {project_id}\n\n"
            brief += "## Core Principles & Architecture\n"
            for s in summaries:
                brief += f"- {s.content}\n"
                
            return {"brief": brief}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/impact", dependencies=[Depends(verify_api_key)])
async def run_impact_analysis(project_id: str, principle: str):
    """
    Placeholder for v4.0 Impact Analysis logic.
    In a real app, this would query the Apache Age graph to find nodes impacted by a change.
    """
    try:
        return {
            "status": "success",
            "impacted_areas": [
                {"file": "AuthService.py", "reason": "Directly implements this logic."},
                {"file": "LoginController.ts", "reason": "Uses AuthService for token validation."}
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "alive"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
