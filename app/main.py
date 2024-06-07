from fastapi  import FastAPI

from app.users.router import router as users
from app.bookings.router import router as bookings


app = FastAPI()
app.include_router(users)
app.include_router(bookings)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8080)