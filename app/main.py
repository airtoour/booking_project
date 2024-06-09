from fastapi  import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.users.router import router as users
from app.bookings.router import router as bookings
from app.users.me.router import router as profile
from app.users.admin.router import router as admin
from app.pages.router import router as pages
from app.images.router import router as images
from app.hotels.router import router as hotels

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
app.include_router(hotels)


origins = [
    settings.FRONT_PATH,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Authorization", "Access-Control-Allow-Origin"]
)

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"{settings.REDIS_HOST}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8080)
