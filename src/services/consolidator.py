import os
import json
from sqlmodel import Session, select, create_engine, func
from src.models.memory import Memory
from src.services.llm import ExtractorService
from typing import List
import logging

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/universal_ai_layer")
engine = create_engine(DATABASE_URL)

class ConsolidatorService:
    def __init__(self, threshold: int = 100):
        self.threshold = threshold
        self.extractor = ExtractorService()

    async def check_and_consolidate(self, project_id: str):
        """
        Checks if a project has reached the memory threshold and consolidates if necessary.
        """
        with Session(engine) as session:
            count = session.exec(select(func.count(Memory.id)).where(Memory.project_id == project_id, Memory.is_summary == False)).one()
            
            if count >= self.threshold:
                await self._consolidate(project_id, session)

    async def _consolidate(self, project_id: str, session: Session):
        """
        Performs the actual consolidation/summarization.
        """
        # 1. Fetch the oldest facts that aren't summaries
        memories = session.exec(
            select(Memory)
            .where(Memory.project_id == project_id, Memory.is_summary == False)
            .order_by(Memory.created_at.asc())
            .limit(self.threshold)
        ).all()
        
        memory_texts = [m.content for m in memories]
        
        # 2. Use LLM to summarize into core concepts
        prompt = f"""
        You are an AI Memory Specialist. You are given 100 atomic facts about the project '{project_id}'.
        Your task is to consolidate these into 10 high-level "Core Principles" or "Architectural Concepts".
        These summaries should be durable and represent the essence of the project's engineering state.
        
        Facts:
        {json.dumps(memory_texts)}
        
        Output JSON format:
        {{
            "summaries": [
                {{ "content": "The system architecture follows a modular micro-service pattern.", "importance": 1.0 }},
                {{ "content": "Database migrations are managed via Prisma and PostgreSQL.", "importance": 0.9 }}
            ]
        }}
        """
        
        response_content = await self.extractor._call_llm(prompt, json_mode=True)
        summary_data = json.loads(response_content).get("summaries", [])
        
        # 3. Store summaries and mark old memories as lower importance or delete
        for item in summary_data:
            embedding = await self.extractor.get_embedding(item["content"])
            import hashlib
            fact_hash = hashlib.sha256(item["content"].lower().strip().encode()).hexdigest()
            
            summary_memory = Memory(
                content=item["content"],
                cleaned_content=item["content"].lower(),
                embedding=embedding,
                project_id=project_id,
                hash=fact_hash,
                is_summary=True,
                importance_score=item["importance"],
                source="system"
            )
            session.add(summary_memory)
        
        # Optionally: Reduce importance of old memories or archive them
        for m in memories:
            m.importance_score *= 0.5 # Reduce importance as it's now summarized
            
        session.commit()
        logging.info(f"Consolidated {len(memories)} memories for project {project_id}")
