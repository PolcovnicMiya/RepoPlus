from typing import Annotated
from dataclasses import dataclass
from pydantic import Field
from pydantic_settings import BaseSettings


class BD_Settings(BaseSettings):
    DB_HOST : Annotated [str | int , Field (..., env = 'BD_HOST')]
    DB_PORT : Annotated [str | int , Field (..., env = 'BD_PORT')]
    DB_PASS : Annotated [str | int , Field (..., env = 'BD_PASS')]
    DB_USER : Annotated [str | int , Field (..., env = 'BD_USER')]
    DB_NAME : Annotated [str | int , Field (..., env = 'BD_NAME')]
    TestDB_HOST : Annotated [str | int , Field (..., env = 'TestBD_HOST')]
    TestDB_PORT : Annotated [str | int , Field (..., env = 'TestBD_PORT')]
    TestDB_PASS : Annotated [str | int , Field (..., env = 'TestBD_PASS')]
    TestDB_USER : Annotated [str | int , Field (..., env = 'TestBD_USER')]
    TestDB_NAME : Annotated [str | int , Field (..., env = 'TestBD_NAME')]



db_setting = BD_Settings()

@dataclass
class Postgres:
    DB_HOST : str = db_setting.DB_HOST
    DB_PORT : str = db_setting.DB_PORT
    DB_PASS : str = db_setting.DB_PASS
    DB_USER : str = db_setting.DB_USER
    DB_NAME : str = db_setting.DB_NAME

@dataclass
class TestPostgres:
    TestDB_HOST : str = db_setting.TestDB_HOST
    TestDB_PORT : str = db_setting.TestDB_PORT
    TestDB_PASS : str = db_setting.TestDB_PASS
    TestDB_USER : str = db_setting.TestDB_USER
    TestDB_NAME : str = db_setting.TestDB_NAME


class Setting:
    def __init__(self):
        self.pg = Postgres()
        self.tpg = TestPostgres()

settings : Setting = Setting()
