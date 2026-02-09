from typing import Optional
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str 
    POSTGRES_PASSWORD: str 
    POSTGRES_DB: str 
    POSTGRES_HOST: str 
    POSTGRES_PORT: int

    MONGO_DB: str 
    MONGO_HOST: str 
    MONGO_PORT: int

    DEBUG: bool = False
    ECHO: bool = False

    class Config:
        env_file = ".env"

    @property
    def POSTGRES_URL(self) -> Optional[PostgresDsn]:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    @property
    def MONGO_URL(self):
        return(
            f"mongodb://{self.MONGO_HOST}:{self.MONGO_PORT}/?directConnection=true"
        )

config = Settings()