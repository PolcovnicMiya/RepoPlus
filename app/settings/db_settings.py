from dataclasses import dataclass
import os
from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings
from typing import Annotated

class BD_Settings(BaseSettings):
    DB_HOST : Annotated [str | int , Field (..., env = 'BD_HOST')]
    DB_PORT : Annotated [str | int , Field (..., env = 'BD_PORT')]
    DB_PASS : Annotated [str | int , Field (..., env = 'BD_PASS')]
    DB_USER : Annotated [str | int , Field (..., env = 'BD_USER')]
    DB_NAME : Annotated [str | int , Field (..., env = 'BD_NAME')]
    

    # class ENV:
    #     env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")


db_setting = BD_Settings()

@dataclass
class Postgres:
    DB_HOST : str = db_setting.DB_HOST
    DB_PORT : str = db_setting.DB_PORT
    DB_PASS : str = db_setting.DB_PASS
    DB_USER : str = db_setting.DB_USER
    DB_NAME : str = db_setting.DB_NAME


class Setting:
    def __init__(self):
        self.pg = Postgres()
        
settings : Setting = Setting() 