from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str
    database_url: str

    news_api_key: str = ""
    hunter_api_key: str = ""
    clearbit_api_key: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
