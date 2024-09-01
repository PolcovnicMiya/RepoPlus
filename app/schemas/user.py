from pydantic import BaseModel, EmailStr

class CreateUserModel(BaseModel):
    username: str
    password: str
    email: EmailStr
    in_match: bool
