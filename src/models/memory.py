from typing import Optional, List
from sqlmodel import SQLModel, Field, Column
from pgvector.sqlalchemy import Vector
import sqlalchemy as sa
from datetime import datetime

class Memory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    cleaned_content: str  # For keyword search
    embedding: List[float] = Field(sa_column=Column(Vector(1536)))  # OpenAI standard
    
    # Scoping
    user_id: Optional[str] = Field(default=None, index=True)
    session_id: Optional[str] = Field(default=None, index=True)
    project_id: Optional[str] = Field(default=None, index=True)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    hash: str = Field(unique=True, index=True) # SHA256 for deduplication
    
    # Engineering Focus
    is_conflict: bool = Field(default=False)
    source: str = Field(default="user") # e.g., "user", "git", "system"
    module: Optional[str] = Field(default=None) # e.g., "auth", "db"
    
    # v3.0 Intelligence
    importance_score: float = Field(default=0.5) # 0.0 to 1.0
    is_summary: bool = Field(default=False)
    is_validated: Optional[bool] = Field(default=None) # None = Pending, True = Approved, False = Rejected
    
    # v4.0 XAI & Traceability
    source_ref: Optional[str] = Field(default=None) # Commit hash, Issue URL, etc.
