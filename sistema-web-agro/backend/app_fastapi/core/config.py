from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # The shared dotenv also configures the legacy backend and LLM providers.
    model_config = SettingsConfigDict(env_file='.env', extra='ignore', hide_input_in_errors=True)
    APP_MODE: str = "EXPERIMENT"
    SECRET_KEY: str = "agro-intelligence-secret-2026-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/agro_audit"

settings = Settings()
