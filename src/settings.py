from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "購物網站後端"
    app_description: str = "小破站"
    app_version: str = "1.0.0"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    db_connection: str = "sqlite:///app.sqlite3"

    mail_username: str = ""
    mail_password: str = ""
    mail_from: str = ""
    mail_port: int = 25
    mail_server: str = ""
    mail_starttls: bool = False
    mail_ssl_tls: bool = False
    mail_use_credentials: bool = False
    mail_validate_certs: bool = False

    model_config = SettingsConfigDict(env_file=".env")

    secret_key: str
    algorithm: str = "SHA256"
    access_token_expire_minutes: int
    

settings = Settings()