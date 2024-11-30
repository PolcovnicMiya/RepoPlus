from pydantic import BaseModel, EmailStr

class CreateUserModel(BaseModel):
    username: str
    password: str
    email: EmailStr
    phone: int
    name: str
    lastname: str
    card_number: int
    balance: float
    photo: str
    is_verified: bool = False

    class Config:
        from_attributes = True