from app.repository.user import UserRepository,user_repo
from app.service.login import LoginService
from app.service.register import RegisterService
from app.secure.jwt_helper import Jwt, jwt_use
def login_service():
    return LoginService(UserRepository,jwt_use)

def register_service():
    return RegisterService(UserRepository,jwt_use)