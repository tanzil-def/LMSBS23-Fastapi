from pydantic import BaseSettings

class Settings(BaseSettings):
    MYSQL_URL: str = "mysql+pymysql://libraryuser:StrongPassword123@localhost/library"
    SECRET_KEY: str = "your_super_secret_key_here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
