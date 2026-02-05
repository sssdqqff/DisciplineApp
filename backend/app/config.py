from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My Awesome App"
    debug_mode: bool = False
    database_url: str = "postgresql+asyncpg://postgres:subbotin@localhost:5432/postgres"
    cors_origins: list = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]
    static_dir: str = "static"
    images_dir: str = "static/images"

    # Переменные для авторизации
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"

# создаём объект настроек
settings = Settings()

# для удобного импорта в security.py
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
