from datetime import date
from sqlalchemy import and_, func, or_, select
from sqlalchemy.exc import SQLAlchemyError

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker, engine
from app.hotels.rooms.models import Rooms
from app.logger import logger


class RoomDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_all(
        cls,
        hotel_id: int,
        date_from: date,
        date_to: date
    ):
        try:
            booked_rooms = (
                select(Bookings.room_id, func.count(Bookings.room_id).label("rooms_booked"))
                .select_from(Bookings)
                .where(
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to,
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from,
                        ),
                    ),
                )
                .group_by(Bookings.room_id)
                .cte("booked_rooms")
            )

            get_rooms = (
                select(
                    Rooms.__table__.columns,
                    (Rooms.price * (date_to - date_from).days).label("total_cost"),
                    (Rooms.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)).label("rooms_left"),
                )
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                .where(
                    Rooms.hotel_id == hotel_id
                )
            )

            async with async_session_maker() as session:
                logger.debug(get_rooms.compile(engine, compile_kwargs={"literal_binds": True}))
                rooms = await session.execute(get_rooms)
                return rooms.mappings().all()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                message = "Database"
            elif isinstance(e, Exception):
                message = "Unknown"
            message += "Exc: Cannot find Rooms"
            extra = {
                "hotel_id": hotel_id,
                "date_from": date_from,
                "date_to": date_to
            }
            logger.error(message, extra=extra, exc_info=True)
