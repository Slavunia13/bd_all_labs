from fastapi.security import OAuth2PasswordBearer
from pydantic_settings import BaseSettings, SettingsConfigDict


class DefaultSettings(BaseSettings):
    REDIS_NAME: str 
    REDIS_HOST: str 
    REDIS_PORT: int 

    BACKEND_NAME: str 
    BACKEND_HOST: str 
    BACKEND_PORT: int 

    MONGO_NAME: str
    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_USER: str
    MONGO_PASSWORD: str

    PATH_PREFIX: str 

    model_config = SettingsConfigDict(env_file=".env")