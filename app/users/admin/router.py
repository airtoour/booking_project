from fastapi import APIRouter, Depends
from app.users.models import Users
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_admin_user


router = APIRouter(
    prefix="/admin",
    tags=["Админ"]
)

@router.get("/all")
async def read_users_all(current_user: Users = Depends(get_current_admin_user)):
    return await UsersDAO.find_all()