from sqlalchemy import delete

from app.dao.base import BaseDAO
from app.bookings.models import Bookings
from app.users.models import Users
from app.database import async_session_maker


class UsersDAO(BaseDAO):
    model = Users

    @staticmethod
    async def delete(user_id: int):
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
