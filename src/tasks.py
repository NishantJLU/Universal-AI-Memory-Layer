from src.celery_app import celery_app
from src.services.consolidator import ConsolidatorService
from src.services.conflict_resolver import ConflictResolver
import asyncio

# Helper to run async code in sync celery tasks
def run_async(coro):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coro)

@celery_app.task(name="tasks.consolidate")
def consolidate_task(project_id: str):
    consolidator = ConsolidatorService()
    run_async(consolidator.check_and_consolidate(project_id))

from src.services.watchdogs.slack_bot import SlackWatchdog
import asyncio

# ... (previous imports)

@celery_app.task(name="tasks.audit_conflicts")
def audit_conflicts_task(project_id: str):
    resolver = ConflictResolver()
    run_async(resolver.audit_memories(project_id))

@celery_app.task(name="tasks.generate_reports")
def generate_reports_task():
    # In a real app, you'd iterate over all projects
    # For now, we'll use a placeholder project_id or fetch from DB
    watchdog = SlackWatchdog()
    # run_async(watchdog.post_daily_report("default_project"))
