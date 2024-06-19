from fastapi import APIRouter, Response, Depends

from app.users.schemas import SUserRegister, SUserAuth
from app.users.dao import UsersDAO
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.models import Users
from app.users.dependencies import get_current_user
from app.exceptions import UserAlreadyExistsException, IncorrectUserEmailOrPasswordException, NotExistingUser


router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"]
)

@router.post("/register")
async def register_user(user_data: SUserRegister):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectUserEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)

    return access_token


@router.delete("/delete")
async def delete_user(response: Response, user_id: Users = Depends(get_current_user)):
    existing_user = await UsersDAO.find_one_or_none(id=user_id.id)
    if existing_user:
        await UsersDAO.delete(user_id.id)
        response.delete_cookie("booking_access_token")
    else:
        raise NotExistingUser
    return "Пользователь успешно удалён!"


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")
    return "Вы вышли из системы!"
