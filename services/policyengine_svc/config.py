from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    policyengine_url: str = "http://127.0.0.1:8080"
    cors_origins: list[str] = ["*"]

def get_settings() -> Settings:
    return Settings()
