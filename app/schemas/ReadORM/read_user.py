from pydantic import BaseModel, EmailStr


class ReadUSerModel(BaseModel):
    username: str
    password: str
    email: EmailStr
    in_match: bool

    class Config:
        from_attributes = True
