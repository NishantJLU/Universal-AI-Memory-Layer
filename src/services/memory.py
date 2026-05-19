from sqlmodel import Session, select, create_engine, SQLModel
from src.models.memory import Memory
from src.services.llm import ExtractorService
from src.services.graph import GraphService
from src.tasks import consolidate_task, audit_conflicts_task
import hashlib
import json
from datetime import datetime
from typing import List, Optional
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/universal_ai_layer")
engine = create_engine(DATABASE_URL)

class MemoryService:
    def __init__(self):
        self.extractor = ExtractorService()
        self.graph = GraphService()

    def _generate_hash(self, content: str) -> str:
        return hashlib.sha256(content.lower().strip().encode()).hexdigest()

    async def add_memory(self, 
                         raw_text: str, 
                         user_id: str = None, 
                         session_id: str = None, 
                         project_id: str = None,
                         source: str = "user"):
        # 1. Extract atomic facts
        facts = await self.extractor.extract_facts(raw_text)
        
        # 2. Extract entities for graph
        graph_data = await self.extractor.extract_entities(raw_text)
        
        # Process Graph Data (Apache Age)
        self._process_graph(graph_data, project_id)
        
        with Session(engine) as session:
            # Handle Memories (Vector/Relational logic)
            for fact in facts:
                fact_hash = self._generate_hash(fact)
                
                # Deduplication check
                existing = session.exec(select(Memory).where(Memory.hash == fact_hash)).first()
                if existing:
                    continue
                
                embedding = await self.extractor.get_embedding(fact)
                
                new_memory = Memory(
                    content=fact,
                    cleaned_content=fact.lower(),
                    embedding=embedding,
                    user_id=user_id,
                    session_id=session_id,
                    project_id=project_id,
                    hash=fact_hash,
                    source=source
                )
                session.add(new_memory)
            
            session.commit()
        
        # v4.0: Trigger Async Tasks
        if project_id:
            consolidate_task.delay(project_id)
            audit_conflicts_task.delay(project_id)

    async def _check_deviations(self, fact: str, project_id: str, session: Session) -> bool:
        """
        Checks if a new fact deviates from core architectural principles.
        """
        # 1. Fetch core summaries for context
        summaries = session.exec(
            select(Memory)
            .where(Memory.project_id == project_id, Memory.is_summary == True)
            .order_by(Memory.importance_score.desc())
            .limit(5)
        ).all()
        
        if not summaries:
            return False
            
        summary_texts = [s.content for s in summaries]
        
        prompt = f"""
        Does the new fact contradict any of the project's core principles?
        Core Principles: {json.dumps(summary_texts)}
        New Fact: {fact}
        
        Answer with JSON: {{"deviates": true/false, "reason": "..."}}
        """
        
        response_content = await self.extractor._call_llm(prompt, json_mode=True)
        result = json.loads(response_content)
        return result.get("deviates", False)

    def _process_graph(self, graph_data, project_id):
        # Implementation for adding entities and relationships to Apache Age
        for ent in graph_data.get("entities", []):
            self.graph.add_entity(ent["name"], ent["type"], project_id)
        
        for rel in graph_data.get("relations", []):
            self.graph.add_relation(rel["source"], rel["target"], rel["type"], project_id)

    def _check_conflicts(self, fact: str, project_id: str, session: Session) -> bool:
        # Placeholder for conflict detection logic
        # Real logic is now in ConflictResolver service
        return False
