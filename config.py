from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    JWT_KEY: str
    JWT_ALGORITHM: str

    TEMPLATE_PATH: str
    STATIC_PATH: str
    STATIC_IMAGES_PATH: str

    class Config:
        env_file = 'D:/FastAPI/booking_project_pet/.env'


settings = Settings()
