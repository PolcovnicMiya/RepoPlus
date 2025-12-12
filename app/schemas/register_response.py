from pydantic import BaseModel


class RegisterResponseModel(BaseModel):
    user_id: int
    message: str = "Пользователь успешно зарегистрирован"

    class Config:
        from_attributes = True