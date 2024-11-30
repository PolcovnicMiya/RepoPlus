from app.model.user import User
from .repo import SQLAlchemyRepo
from .test_repo import SQLAlchemyRepoPlus


class UserRepository(SQLAlchemyRepo):
    model = User


user_repo = UserRepository()


class UserRepositoryPlus(SQLAlchemyRepoPlus):
    model = User


user_repo_plus = UserRepositoryPlus()
