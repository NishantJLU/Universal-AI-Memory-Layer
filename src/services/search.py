from sqlmodel import Session, select, create_engine, text
from src.models.memory import Memory
from src.services.llm import ExtractorService
from src.services.graph import GraphService
from typing import List, Dict, Any
import os
import numpy as np
import hashlib
import redis
import json

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/universal_ai_layer")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
engine = create_engine(DATABASE_URL)

class SearchService:
    def __init__(self):
        self.extractor = ExtractorService()
        self.graph = GraphService()
        self.redis_client = redis.from_url(REDIS_URL)

    def _get_cache_key(self, query: str, project_id: str) -> str:
        return f"search_cache:{hashlib.md5(f'{query}:{project_id}'.encode()).hexdigest()}"

    async def hybrid_search(self, 
                            query: str, 
                            project_id: str = None, 
                            limit: int = 5) -> Dict[str, Any]:
        """
        Triple-Hybrid Search with Distributed Semantic Cache (v4.0):
        1. Vector Similarity (Semantic)
        2. Keyword Match (Precision)
        3. Graph Traversal (Context)
        """
        cache_key = self._get_cache_key(query, project_id)
        cached_response = self.redis_client.get(cache_key)
        if cached_response:
            return json.loads(cached_response)

        query_embedding = await self.extractor.get_embedding(query)
        
        with Session(engine) as session:
            # 1. Vector Search (Semantic)
            vector_query = text("""
                SELECT id, content, created_at, 
                (embedding <=> :embedding) as distance
                FROM memory
                WHERE (:project_id IS NULL OR project_id = :project_id)
                ORDER BY distance ASC
                LIMIT :limit
            """)
            vector_results = session.execute(vector_query, {
                "embedding": str(query_embedding),
                "project_id": project_id,
                "limit": limit
            }).fetchall()

            # 2. Keyword Search (FTS)
            keyword_query = select(Memory).where(
                Memory.content.ilike(f"%{query}%")
            )
            if project_id:
                keyword_query = keyword_query.where(Memory.project_id == project_id)
            keyword_results = session.exec(keyword_query.limit(limit)).all()

            # 3. Graph Context (Entities) via Apache Age
            entity_data = await self.extractor.extract_entities(query)
            graph_context = []
            for ent in entity_data.get("entities", []):
                related = self.graph.get_related_entities(ent["name"], project_id)
                for item in related:
                    graph_context.append(f"Related to {ent['name']}: {item}")

            # 4. Fusion & Ranking (v4.0 XAI)
            combined_results = []
            seen_ids = set()

            for res in vector_results:
                if res.id not in seen_ids:
                    # Fetch source_ref for traceability
                    mem = session.get(Memory, res.id)
                    combined_results.append({
                        "id": res.id,
                        "content": res.content,
                        "score": 1 - res.distance,
                        "score_breakdown": {
                            "vector_similarity": 1 - res.distance,
                            "keyword_match": 0,
                            "graph_boost": 0
                        },
                        "source_ref": mem.source_ref if mem else None,
                        "type": "vector"
                    })
                    seen_ids.add(res.id)

            for res in keyword_results:
                if res.id in seen_ids:
                    # Update score breakdown for existing result
                    for item in combined_results:
                        if item["id"] == res.id:
                            item["score"] += 0.2 # Keyword boost
                            item["score_breakdown"]["keyword_match"] = 0.2
                else:
                    combined_results.append({
                        "id": res.id,
                        "content": res.content,
                        "score": 0.8,
                        "score_breakdown": {
                            "vector_similarity": 0,
                            "keyword_match": 0.8,
                            "graph_boost": 0
                        },
                        "source_ref": res.source_ref,
                        "type": "keyword"
                    })
                    seen_ids.add(res.id)

            response = {
                "results": sorted(combined_results, key=lambda x: x["score"], reverse=True),
                "graph_context": list(set(graph_context))
            }
            
            # Store in Redis cache (expiry 1 hour)
            self.redis_client.setex(cache_key, 3600, json.dumps(response))
            return response
