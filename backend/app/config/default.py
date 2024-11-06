from fastapi.security import OAuth2PasswordBearer
from pydantic_settings import BaseSettings, SettingsConfigDict


class DefaultSettings(BaseSettings):
    NEO4J_NAME: str
    NEO4J_HOST: str
    NEO4J_AUTH: str
    NEO4J_dbms_memory_heap_initial__size: str
    NEO4J_dbms_memory_heap_max__size: str
    NEO4J_PORT_HTTP: int
    NEO4J_PORT_BOLT: int

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