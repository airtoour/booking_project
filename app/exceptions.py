from fastapi import HTTPException, status

class BookingExceptions(HTTPException):
    status_code = 500
    detail = "Ошибка на сервере, извините :("

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingExceptions):
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь уже зарегистрирован!"

class IncorrectUserEmailOrPasswordException(BookingExceptions):
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверная почта или пароль"

class TokenAbsentException(BookingExceptions):
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен отсутствует!"

class ExpiredTokenException(BookingExceptions):
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен истёк!"

class IncorrectTokenFormatException(BookingExceptions):
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверный формат токена!"


class NotExistingUser(BookingExceptions):
    status_code=status.HTTP_401_UNAUTHORIZED