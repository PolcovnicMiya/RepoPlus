from datetime import datetime
from sqlalchemy import String, DECIMAL, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.model.base import Base


class CartItem(Base):
    __tablename__ = 'cart_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    
    # Настройки размера
    size_type: Mapped[str] = mapped_column(String(50), nullable=True)  # "grande", "venti"
    size_price_modifier: Mapped[float] = mapped_column(DECIMAL(10, 2), default=0.0, nullable=False)
    
    # Настройки кофе
    coffee_type: Mapped[str] = mapped_column(String(50), nullable=True)  # "espresso_roast", "decaf", "none"
    coffee_shots: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    coffee_price_modifier: Mapped[float] = mapped_column(DECIMAL(10, 2), default=0.0, nullable=False)
    
    # Настройки молока
    milk_type: Mapped[str] = mapped_column(String(50), nullable=True)  # "regular", "low_fat", "soy", "oat", "coconut"
    milk_price_modifier: Mapped[float] = mapped_column(DECIMAL(10, 2), default=0.0, nullable=False)
    
    # Настройки сиропа
    syrup_type: Mapped[str] = mapped_column(String(50), nullable=True)  # "none", "caramel", "mint", "raspberry", "coconut", "sugar"
    syrup_price_modifier: Mapped[float] = mapped_column(DECIMAL(10, 2), default=0.0, nullable=False)
    
    # Итоговая цена
    total_price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    
    # Связи
    user: Mapped["User"] = relationship("User", back_populates="cart_items")
    product: Mapped["Product"] = relationship("Product", back_populates="cart_items")

    def to_read_model(self):
        from app.schemas.ReadORM.read_cart import ReadCartItemModel
        return ReadCartItemModel(
            id=self.id,
            user_id=self.user_id,
            product_id=self.product_id,
            quantity=self.quantity,
            size_type=self.size_type,
            size_price_modifier=float(self.size_price_modifier),
            coffee_type=self.coffee_type,
            coffee_shots=self.coffee_shots,
            coffee_price_modifier=float(self.coffee_price_modifier),
            milk_type=self.milk_type,
            milk_price_modifier=float(self.milk_price_modifier),
            syrup_type=self.syrup_type,
            syrup_price_modifier=float(self.syrup_price_modifier),
            total_price=float(self.total_price),
            created_at=self.created_at
        )