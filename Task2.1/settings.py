from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.override"),
        env_file_encoding="utf-8",
    )

    base_url: str = "https://qa-internship.avito.com"


base_settings = Settings()
