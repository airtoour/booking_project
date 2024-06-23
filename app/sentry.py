import sentry_sdk

from main import app
from app.config import settings


sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0