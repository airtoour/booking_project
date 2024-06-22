from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError

from app.dao.base import BaseDAO
from app.bookings.models import Bookings
from app.logger import logger
from app.users.models import Users
from app.database import async_session_maker


class UsersDAO(BaseDAO):
    model = Users

    @staticmethod
    async def delete(user_id: int):
        try:
            async with async_session_maker() as session:
                delete_bookings = (
                    delete(Bookings).
                    where(Bookings.user_id == user_id)
                )
                delete_user = (
                    delete(Users).
                    where(Users.id == user_id)
                )

                await session.execute(delete_bookings)
                await session.execute(delete_user)

                await session.commit()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                message = "Database"
            elif isinstance(e, Exception):
                message = "Unknown"
            message += "Exception: Cannot Delete User"

            extra = {
                "user_id": user_id,
            }
            logger.error(message, extra=extra, exc_info=True)
