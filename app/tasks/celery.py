from celery import Celery
from config import settings


celery = Celery(
    "tasks",
    broker=f"{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=["app.tasks.tasks"]
)
