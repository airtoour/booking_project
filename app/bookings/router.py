from fastapi import APIRouter, Depends, BackgroundTasks
from datetime import date
from pydantic import parse_obj_as

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.users.models import Users
from app.users.dependencies import get_current_user
from app.exceptions import RoomCannotBeBooked
from app.tasks.tasks import send_booking_confirmation_email
from app.config import settings

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)):
    return await BookingDAO.find_all(user_id=user.id)


@router.post("")
async def add_booking(
    background_tasks: BackgroundTasks,
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user)
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)

    if not booking:
        raise RoomCannotBeBooked

    booking_dict = parse_obj_as(SBooking, booking).dict()
    # Celery
    # send_booking_confirmation_email.delay(booking_dict, settings.SMTP_USER)

    # BgTasks
    background_tasks.add_task(send_booking_confirmation_email(booking_dict, settings.SMTP_USER))

    return booking_dict