from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_MODE: str = "EXPERIMENT"
    SECRET_KEY: str = "agro-intelligence-secret-2026-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/agro_audit"

    class Config:
        env_file = ".env"

settings = Settings()
