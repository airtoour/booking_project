from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = "Ошибка на сервере, извините :("

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT,
    detail = "Пользователь уже зарегистрирован!"

class IncorrectUserEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = "Неверная почта или пароль!"

class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = "Токен отсутствует!"

class ExpiredTokenException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = "Токен истёк!"

class IncorrectTokenFormatException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = "Неверный формат токена!"

class NotExistingUser(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED

class RoomCannotBeBooked(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных номеров!"

class DateFromCannotBeAfterDateTo(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Дата заезда не может быть позже даты выезда"

class CannotBookHotelForLongPeriod(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Невозможно забронировать отель сроком более месяца"

class CannotAddDataToDatabase(BookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось добавить запись"

class CannotProcessCSV(BookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось обработать CSV файл"