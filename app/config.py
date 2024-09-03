from typing import Literal

from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()

class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    JWT_KEY: str
    JWT_ALGORITHM: str

    TEMPLATE_PATH: str
    STATIC_PATH: str
    STATIC_IMAGES_PATH: str

    FRONT_PATH: str

    REDIS_HOST: str
    REDIS_PORT: int

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    SENTRY_DSN: str

    model_config = ConfigDict(from_attributes=True)


settings = Settings()
