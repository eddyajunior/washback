from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Lava Rápido IA"

    DATABASE_URL: str = "sqlite:///./lava_rapido.db"

    SECRET_KEY: str = "super-secret-key"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()