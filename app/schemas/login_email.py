from pydantic import BaseModel, EmailStr, Field
from typing import Annotated


class LoginEmailSchema(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=1, max_length=255)]

    class Config:
        from_attributes = True