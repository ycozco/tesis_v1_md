from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr, field_validator
import secrets

class Settings(BaseSettings):
    # The shared dotenv also configures the legacy backend and LLM providers.
    model_config = SettingsConfigDict(env_file='.env', extra='ignore', hide_input_in_errors=True)
    APP_MODE: str = "EXPERIMENT"
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(48))
    @field_validator('SECRET_KEY', mode='before')
    @classmethod
    def nonempty_signing_key(cls, value):
        return value if isinstance(value, str) and value.strip() else secrets.token_urlsafe(48)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/agro_audit"
    RESEARCH_ALLOW_LOCAL_AI: bool = False
    RESEARCH_OLLAMA_MODEL: str = ''
    RESEARCH_ALLOW_PAID_AI: bool = False
    RESEARCH_DEEPSEEK_MODEL: str = 'deepseek-flash'
    RESEARCH_DEEPSEEK_API_KEY: SecretStr = SecretStr('')

settings = Settings()
