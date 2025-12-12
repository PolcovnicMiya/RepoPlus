from datetime import datetime
from pydantic import BaseModel, EmailStr


class ReadUserModel(BaseModel):
    id: int
    name: str
    lastname: str
    email: EmailStr
    password: str
    doc: datetime
    is_verified: bool

    class Config:
        from_attributes = True