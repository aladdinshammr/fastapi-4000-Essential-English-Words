from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_host: str = ""
    database_port: str = ""
    database_name: str = ""
    database_user: str = ""
    database_password: str = ""
    base_url: str = ""
    secret_key: str = ""
    algorithm: str = ""
    access_token_expire_minutes: int = 0

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
