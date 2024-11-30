import os
from pathlib import Path
from typing import Annotated
from dataclasses import dataclass
from pydantic import Field
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent.parent


class BD_Settings(BaseSettings):
    DB_HOST: Annotated[str | int, Field(..., env="BD_HOST")]
    DB_PORT: Annotated[str | int, Field(..., env="BD_PORT")]
    DB_PASS: Annotated[str | int, Field(..., env="BD_PASS")]
    DB_USER: Annotated[str | int, Field(..., env="BD_USER")]
    DB_NAME: Annotated[str | int, Field(..., env="BD_NAME")]

    TestDB_HOST: Annotated[str | int, Field(..., env="TestBD_HOST")]
    TestDB_PORT: Annotated[str | int, Field(..., env="TestBD_PORT")]
    TestDB_PASS: Annotated[str | int, Field(..., env="TestBD_PASS")]
    TestDB_USER: Annotated[str | int, Field(..., env="TestBD_USER")]
    TestDB_NAME: Annotated[str | int, Field(..., env="TestBD_NAME")]

    PUBLIC_KEY_PATH: Path = BASE_DIR / "app" / "secure" / "keys" / "jwt-public.pem"
    PRIVATE_KEY_PATH: Path = BASE_DIR / "app" / "secure" / "keys" / "jwt-private.pem"
    ALGORITM: str = Field(..., env="ALGORITM")
    ACCESS_TOKEN_EXPIRE_IN_MINUTES: int = Field(
        ..., env="ACCESS_TOKEN_EXPIRE_IN_MINUTES"
    )
    REFRESH_TOKEN_EXPIRE_IN_DAYS: int = Field(..., env="REFRESH_TOKEN_EXPIRE_IN_DAYS")

    DB_HOST: Annotated[str | int, Field(..., env="BD_HOST")]
    DB_PORT: Annotated[str | int, Field(..., env="BD_PORT")]
    DB_PASS: Annotated[str | int, Field(..., env="BD_PASS")]
    DB_USER: Annotated[str | int, Field(..., env="BD_USER")]
    DB_NAME: Annotated[str | int, Field(..., env="BD_NAME")]

    REDIS_HOST: Annotated[str | int, Field(..., env="REDIS_HOST")]
    REDIS_PORT: Annotated[str | int, Field(..., env="REDIS_PORT")]
    REDIS_BD: Annotated[str | int, Field(..., env="REDIS_BD")]

    SMTP_EMAIL: str = Field(..., env="SMTP_EMAIL")
    SMTP_EMAILPASSWOR: str = Field(..., env="SMTP_EMAILPASSWOR")
    SMTP_PORT: int = Field(..., env="SMTP_PORT")
    SMTP_HOST: str = Field(..., env="SMTP_HOST")

    class Config:
        env_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"
        )


db_setting = BD_Settings()


@dataclass
class Postgres:
    DB_HOST: str = db_setting.DB_HOST
    DB_PORT: str = db_setting.DB_PORT
    DB_PASS: str = db_setting.DB_PASS
    DB_USER: str = db_setting.DB_USER
    DB_NAME: str = db_setting.DB_NAME


@dataclass
class TestPostgres:
    TestDB_HOST: str = db_setting.TestDB_HOST
    TestDB_PORT: str = db_setting.TestDB_PORT
    TestDB_PASS: str = db_setting.TestDB_PASS
    TestDB_USER: str = db_setting.TestDB_USER
    TestDB_NAME: str = db_setting.TestDB_NAME


@dataclass
class JWT_Config:
    PUBLIC_KEY_PATH: Path = db_setting.PUBLIC_KEY_PATH
    PRIVATE_KEY_PATH: Path = db_setting.PRIVATE_KEY_PATH
    ALGORITM: str = db_setting.ALGORITM
    ACCESS_TOKEN_EXPIRE_IN_MINUTES: str = db_setting.ACCESS_TOKEN_EXPIRE_IN_MINUTES
    REFRESH_TOKEN_EXPIRE_IN_DAYS: str = db_setting.REFRESH_TOKEN_EXPIRE_IN_DAYS


@dataclass
class Redis_Config:
    REDIS_HOST: str = db_setting.REDIS_HOST
    REDIS_PORT: str = db_setting.REDIS_PORT
    REDIS_BD: str = db_setting.REDIS_BD


@dataclass
class SMTP_Config:
    SMTP_EMAIL: str = db_setting.SMTP_EMAIL
    SMTP_EMAILPASSWOR: str = db_setting.SMTP_EMAILPASSWOR
    SMTP_PORT: int = db_setting.SMTP_PORT
    SMTP_HOST: str = db_setting.SMTP_HOST


class Setting:
    def __init__(self):
        self.pg = Postgres()
        self.tpg = TestPostgres()
        self.jwt_config = JWT_Config()
        self.redis_config = Redis_Config()
        self.smtp = SMTP_Config()


settings: Setting = Setting()
