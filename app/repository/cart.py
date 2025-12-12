from app.model.cart import CartItem
from .repo import SQLAlchemyRepo


class CartRepository(SQLAlchemyRepo):
    model = CartItem


cart_repo = CartRepository()