from app.schemas.user import CreateUserModel


class ReadUSerModel(CreateUserModel):
    id: int

    class Config:
        from_attributes = True
