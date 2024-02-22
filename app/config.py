from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = 'Scrapper API'
    admin_email: str = 'techbizznepal@gmail.com'
    db_url: str = 'mysql://rro@sdf'
    scrap_api_token: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
