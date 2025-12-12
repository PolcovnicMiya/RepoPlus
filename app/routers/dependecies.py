from app.repository.user import UserRepository,user_repo
from app.repository.product import ProductRepository
from app.repository.cart import CartRepository
from app.service.login import LoginService
from app.service.register import RegisterService
from app.service.product import ProductService
from app.service.cart import CartService
from app.secure.jwt_helper import Jwt, jwt_use

def login_service():
    return LoginService(UserRepository,jwt_use)

def register_service():
    return RegisterService(UserRepository,jwt_use)

def product_service():
    return ProductService(ProductRepository, jwt_use)

def cart_service():
    return CartService(CartRepository, jwt_use)