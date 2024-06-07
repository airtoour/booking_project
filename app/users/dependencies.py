from datetime import datetime
from fastapi import Request, Depends
from jose import jwt, JWTError

from config import settings
from app.users.dao import UsersDAO
from app.users.models import Users
from app.exceptions import (TokenAbsentException, ExpiredTokenException,
                            IncorrectTokenFormatException, NotExistingUser)


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")

    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.JWT_KEY, settings.JWT_ALGORITHM)
    except JWTError:
        raise IncorrectTokenFormatException

    expire: str = payload.get("exp")
    if (not expire) and (int(expire) < datetime.utcnow().timestamp()):
        raise ExpiredTokenException

    user_id: str = payload.get("sub")
    if not user_id:
        raise NotExistingUser

    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise NotExistingUser

    return user


async def get_current_admin_user(current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise NotExistingUser
    return current_user