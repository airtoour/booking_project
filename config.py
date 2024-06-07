from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    JWT_KEY: str
    JWT_ALGORITHM: str

    class Config:
        env_file = 'D:/LEARNING/ShumeykoFASTAPI/FASTAPI/learn_fastapi/.env'


settings = Settings()
