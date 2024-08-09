from datetime import datetime
from pydantic import BaseModel, EmailStr

class ReadUSerModel(BaseModel):
    username : str
    password : str
    email : str
    doc : datetime
    in_match : bool

    class Config:
        from_attributes = True