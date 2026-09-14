from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Scrapper API"
    admin_email: str = "admin@example.com"
    db_url: str = "sqlite:///./scrapper.db"
    scrap_api_token: str = ""

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
