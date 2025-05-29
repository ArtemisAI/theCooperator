"""Application settings, powered by Pydantic.

Usage (later):
    from app.core.config import settings
    print(settings.POSTGRES_DSN)
"""

from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Environment-driven settings with sane defaults."""

    # Web
    APP_NAME: str = "theCooperator API"
    BACKEND_CORS_ORIGINS: list[str] = Field(default_factory=list)

    # Database
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "cooperator"
    POSTGRES_PASSWORD: str = "changeme"
    POSTGRES_DB: str = "coop"

    # Auth
    JWT_SECRET: str = "changeme-super-secret"  # pragma: allowlist secret
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # Celery / Redis broker URL for background jobs
    CELERY_BROKER_URL: str = "redis://redis:6379/0"

    # ------------------------------------------------------------------
    # Derived settings computed from the env-vars above.
    # ------------------------------------------------------------------

    @property
    def DSN_ASYNC(self) -> str:  # noqa: N802
        """Async DSN for SQLAlchemy (asyncpg driver)."""

        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def DSN_SYNC(self) -> str:  # noqa: N802
        """Sync DSN for tools that do not yet support async (e.g. Alembic)."""

        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:  # pylint: disable=missing-function-docstring
    return Settings()


settings = get_settings()
