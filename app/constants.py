import os
from pydantic_settings import BaseSettings

OPENAI_MODEL = "gpt-4.1-2025-04-14"


class Settings(BaseSettings):
    env: str = "dev"
    openai_api_key: str


settings = Settings()