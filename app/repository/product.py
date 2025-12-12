from app.model.product import Product
from .repo import SQLAlchemyRepo


class ProductRepository(SQLAlchemyRepo):
    model = Product


product_repo = ProductRepository()