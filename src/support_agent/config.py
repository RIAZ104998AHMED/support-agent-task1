from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    provider: str = "openrouter"
    openrouter_api_key: str = ""
    openrouter_model: str = "nvidia/nemotron-3-super-120b-a12b:free"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()