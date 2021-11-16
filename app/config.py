from pydantic import BaseConfig
from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    db_hostname: str = os.getenv('HOSTNAME')
    db_port: str = os.getenv('DB_PORT')
    db_username: str = os.getenv('USER')
    db_name: str = os.getenv('DB_NAME')
    db_password: str = os.getenv('PASSWORD')
    secret_key: str = os.getenv('SECRET_KEY')
    algorithm: str = os.getenv('ALGORITHM')
    access_token_expire_minutes: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

settings = Settings()