from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "universal_ai_layer",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["src.tasks"]
)

celery_app.conf.beat_schedule = {
    "daily-intelligence-report": {
        "task": "tasks.generate_reports",
        "schedule": 86400.0, # Every 24 hours
    },
}
