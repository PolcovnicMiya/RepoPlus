from typing import Annotated
from pydantic import EmailStr, BaseModel

class VerifyCode(BaseModel):
    email : EmailStr
    code : Annotated[int , None]