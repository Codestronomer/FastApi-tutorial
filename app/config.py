from pydantic import BaseConfig
from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    db_hostname: str
    db_port: str
    db_name: str
    db_username: str
    db_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

settings = Settings()