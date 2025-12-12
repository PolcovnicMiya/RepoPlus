from datetime import datetime
from sqlalchemy import String, DECIMAL, Boolean, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.model.base import Base


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    old_price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=True)
    image_filename: Mapped[str] = mapped_column(String(255), nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=True)  # рейтинг в процентах (0-100)
    reviews_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    
    # Связь с корзиной
    cart_items: Mapped[list["CartItem"]] = relationship("CartItem", back_populates="product")

    def to_read_model(self):
        from app.schemas.ReadORM.read_product import ReadProductModel
        import base64
        import os
        
        # Определяем путь к изображению
        image_base64 = None
        if self.image_filename:
            image_path = os.path.join("media/products", self.image_filename)
            
            # Если файл не существует, используем дефолтное изображение
            if not os.path.exists(image_path):
                image_path = "media/products/product_1_c4e52102.png"
            
            # Читаем файл и конвертируем в base64
            try:
                with open(image_path, "rb") as image_file:
                    image_data = image_file.read()
                    image_base64 = base64.b64encode(image_data).decode('utf-8')
            except Exception:
                # Если и дефолтное изображение не найдено, оставляем None
                image_base64 = None
        
        return ReadProductModel(
            id=self.id,
            name=self.name,
            description=self.description,
            price=float(self.price),
            old_price=float(self.old_price) if self.old_price else None,
            image_base64=image_base64,
            is_available=self.is_available,
            rating=self.rating,
            reviews_count=self.reviews_count,
            created_at=self.created_at
        )