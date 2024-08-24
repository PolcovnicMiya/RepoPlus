from app.model.user import User
from .repo import SQLAlchemyRepo



class UserRepository(SQLAlchemyRepo):
    model = User


user_repo = UserRepository()
