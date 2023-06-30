import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

STAGING = "STAGING"
DEV = "DEV"
PROD = "PROD"
_ENVIRON = os.getenv("ENVIRON")


class DevSettings(BaseSettings):
    DB_USER: str
    DB_NAME: str
    DB_PSW: str
    DB_HOST: str
    DB_PORT: int

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: str

    DB_URI: str

    class Config:
        env_file = ".env"

    @property
    def DB_URI(cls) -> str:
        if os.getenv("DB_URI") is None:
            return f"postgresql://{cls.DB_USER}:{cls.DB_PSW}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
        cls.DB_URI = os.getenv("DB_URI")
        return cls.DB_URI


class StagingSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_HOST: str
    DB_PORT: int

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: str

    DB_URI: str

    class Config:
        env_file = "stagingenv.file"

    @property
    def DB_URI(cls) -> str:
        return f"postgresql://{cls.POSTGRES_USER}:{cls.POSTGRES_PASSWORD}@postgres:{cls.DB_PORT}/{cls.POSTGRES_DB}"


class Prodsettings(BaseSettings):
    pass

    class Config:
        env_file = "prodenv.file"


class TestSettings(BaseSettings):
    pass


@lru_cache
def get_settings():
    if _ENVIRON == DEV:
        return DevSettings()
    elif _ENVIRON == STAGING:
        return StagingSettings()
    elif _ENVIRON == PROD:
        return Prodsettings()


_settings = get_settings()
