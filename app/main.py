from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_versioning import VersionedFastAPI

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

from app.config import settings


app = FastAPI()

app.include_router(users)
app.include_router(bookings)
app.include_router(profile)
app.include_router(pages)
app.include_router(images)
app.include_router(hotels)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")


app = VersionedFastAPI(
    app,
    version_format="{major}",
    prefix_format="/v{major}"
)

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(HotelsAdmin)

app.mount("/static", StaticFiles(directory=settings.STATIC_PATH), "static")
