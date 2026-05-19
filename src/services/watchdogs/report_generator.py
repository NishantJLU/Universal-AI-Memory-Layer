from sqlmodel import Session, select, create_engine, func
from src.models.memory import Memory
from src.services.llm import ExtractorService
from datetime import datetime, timedelta
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/universal_ai_layer")
engine = create_engine(DATABASE_URL)

class ReportGenerator:
    def __init__(self):
        self.extractor = ExtractorService()

    async def generate_daily_report(self, project_id: str):
        """Generates a summary of all activity in the last 24 hours."""
        yesterday = datetime.utcnow() - timedelta(days=1)
        
        with Session(engine) as session:
            # 1. Fetch new memories
            new_memories = session.exec(
                select(Memory)
                .where(Memory.project_id == project_id, Memory.created_at >= yesterday)
            ).all()
            
            if not new_memories:
                return "No new activity in the last 24 hours."

            # 2. Fetch new conflicts
            new_conflicts = [m for m in new_memories if m.is_conflict]
            
            # 3. Use LLM to summarize the activity
            memory_texts = [m.content for m in new_memories]
            prompt = f"""
            Summarize the following engineering activity from the last 24 hours for project '{project_id}'.
            Highlight key decisions and any conflicts found.
            
            Activity:
            {memory_texts}
            
            Conflicts Found: {len(new_conflicts)}
            """
            
            summary = await self.extractor._call_llm(prompt, json_mode=False)
            
            report = f"# Daily Intelligence Report: {project_id}\n"
            report += f"Date: {datetime.utcnow().strftime('%Y-%m-%d')}\n\n"
            report += "## Summary of Activity\n"
            report += summary
            
            return report
