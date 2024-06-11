from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "購物網站後端"
    app_description: str = "小破站"
    app_version: str = "1.0.0"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    db_connection: str = "sqlite:///database.sqlite3"

    mail_username: str = "jimmy688382"
    mail_password: str = ""
    mail_from: str = "jimmy688382@gmail.com"
    mail_port: int = 587
    mail_server: str = "smtp.gmail.com"
    mail_from_name: str = "2HandPlatform"
    mail_starttls: bool = True
    mail_ssl_tls: bool = False
    mail_use_credentials: bool = True
    mail_validate_certs: bool = True

    secret_key: str = "85c6b39014086ded16f58b0c582ef5a5167b0bdc891b45cc7bc3094bd57f47a3"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    ssl_certfile: str | None = None
    ssl_keyfile: str | None = None
    

settings = Settings()