from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.users.router import router as users
from app.bookings.router import router as bookings
from app.users.me.router import router as profile
from app.pages.router import router as pages
from app.images.router import router as images
from app.hotels.router import router as hotels

from app.database import engine

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from sqladmin import Admin
from app.admin.views import UsersAdmin, BookingsAdmin, RoomsAdmin, HotelsAdmin
from app.admin.auth import authentication_backend

from config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(f"{settings.REDIS_HOST}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    try:
        yield
    finally:
        await redis.close()

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory=settings.STATIC_PATH), "static")

app.include_router(users)
app.include_router(bookings)
app.include_router(profile)

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


admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(HotelsAdmin)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8080)
