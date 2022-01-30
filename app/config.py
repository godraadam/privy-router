from pydantic import BaseSettings

class Settings(BaseSettings):
    STORE_PATH: str
    APP_PORT: int
    APP_HOST: str
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True

settings = Settings()