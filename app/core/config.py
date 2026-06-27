from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    # Gemini
    gemini_api_key: str

    # PostgreSQL
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str = "db"
    postgres_port: int = 5432

    # Redis
    redis_host: str = "redis"
    redis_port: int = 6379

    @property
    def database_url(self) -> str:
        """Собирает URL для asyncpg."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def celery_broker_url(self) -> str:
        """Redis как брокер для Celery."""
        return f"redis://{self.redis_host}:{self.redis_port}/0"

    @property
    def celery_result_backend(self) -> str:
        """Redis как хранилище результатов."""
        return f"redis://{self.redis_host}:{self.redis_port}/1"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()