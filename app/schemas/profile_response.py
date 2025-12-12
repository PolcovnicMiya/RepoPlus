from pydantic import BaseModel, EmailStr


class ProfileResponseModel(BaseModel):
    id: int
    email: EmailStr
    name: str
    lastname: str

    class Config:
        from_attributes = True