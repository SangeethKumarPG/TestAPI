from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://user:password@localhost:5432/blog_db"

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }

settings = Settings()
