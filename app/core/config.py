from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Affirmation Intelligence Platform"
    environment: str = "development"
    database_url: str = "sqlite:///./affirmations.db"

    ai_enabled: bool = True
    openai_api_key: str | None = None
    openai_model: str = "gpt-5.6-luna"

    kafka_enabled: bool = True
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_topic: str = "affirmation-events"

    aws_region: str = "af-south-1"
    s3_bucket_name: str = "change-me-affirmation-intelligence"
    dynamodb_table_name: str = "affirmation-metrics"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
