from pydantic.env_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str
    admin_email: str
    db_url: str
    scrap_api_token: str

    class Config:
        env_file = ".env"


settings = Settings()
