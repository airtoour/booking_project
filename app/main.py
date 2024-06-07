from fastapi  import FastAPI
from fastapi.staticfiles import StaticFiles

from app.users.router import router as users
from app.bookings.router import router as bookings
from app.users.me.router import router as profile
from app.users.admin.router import router as admin
from app.pages.router import router as pages
from app.images.router import router as images

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from config import settings

app = FastAPI()

app.mount("/static", StaticFiles(directory=settings.STATIC_PATH), "static")

app.include_router(users)
app.include_router(bookings)
app.include_router(profile)
app.include_router(admin)

app.include_router(pages)
app.include_router(images)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8080)
