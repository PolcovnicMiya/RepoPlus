from typing import Annotated
from pydantic import BaseModel, EmailStr , Field

class RegisterSchema(BaseModel):
    username: Annotated[str, None] = Field(..., min_length=1, max_length=25)
    password: Annotated[str, None] = Field(..., min_length=8, max_length=25)
    email: EmailStr
    phone: int
    name: str
    lastname: str
    card_number: int
