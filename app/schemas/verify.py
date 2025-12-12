from typing import Annotated
from pydantic import BaseModel

class VerifyCode(BaseModel):
    user_id: int
    code: Annotated[int, None]