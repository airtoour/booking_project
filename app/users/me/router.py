from fastapi import APIRouter, Depends
from app.users.models import Users
from app.users.dependencies import get_current_user

router = APIRouter(
    prefix="/profile",
    tags=["Профиль"]
)

@router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user