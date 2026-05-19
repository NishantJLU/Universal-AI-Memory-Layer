import os
import json
from sqlmodel import Session, select, create_engine
from src.models.memory import Memory
from src.services.llm import ExtractorService
from typing import List, Tuple
import logging

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/universal_ai_layer")
engine = create_engine(DATABASE_URL)

class ConflictResolver:
    def __init__(self):
        self.extractor = ExtractorService()

    async def audit_memories(self, project_id: str):
        """
        Periodically reviews memories in a project to find contradictions.
        """
        with Session(engine) as session:
            # 1. Fetch all memories for the project
            memories = session.exec(select(Memory).where(Memory.project_id == project_id)).all()
            
            if len(memories) < 2:
                return []

            # 2. Batch comparison
            # In a production app, we'd use vector clusters to narrow down potential conflicts
            memory_texts = [f"ID {m.id}: {m.content}" for m in memories]
            
            prompt = f"""
            You are an AI Memory Auditor. Your task is to find contradictory facts within the following list of memories for the project '{project_id}'.
            
            Memories:
            {json.dumps(memory_texts)}
            
            Identify any pairs that logically contradict each other. 
            Format your output as a JSON list of objects:
            {{
                "conflicts": [
                    {{ "id1": 1, "id2": 2, "reason": "Memory 1 says Port 80, Memory 2 says Port 443" }}
                ]
            }}
            If no conflicts exist, return an empty list for "conflicts".
            """
            
            response_content = await self.extractor._call_llm(prompt, json_mode=True)
            conflicts = json.loads(response_content).get("conflicts", [])
            
            # 3. Flag conflicts in the database
            for conflict in conflicts:
                m1 = session.get(Memory, conflict["id1"])
                m2 = session.get(Memory, conflict["id2"])
                if m1: m1.is_conflict = True
                if m2: m2.is_conflict = True
            
            session.commit()
            return conflicts
