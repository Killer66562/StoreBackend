from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "購物網站後端"
    app_description: str = "小破站"
    app_version: str = "1.0.0"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    db_connection: str = "sqlite:///database.sqlite3"

    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int = 587
    mail_server: str = "smtp.gmail.com"
    mail_from_name: str = "2HandPlatform"
    mail_starttls: bool = True
    mail_ssl_tls: bool = False
    mail_use_credentials: bool = True
    mail_validate_certs: bool = True

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    ssl_certfile: str | None = None
    ssl_keyfile: str | None = None

    admin_username: str
    admin_email: str
    admin_password: str

    static_files_root: str
    

settings = Settings()