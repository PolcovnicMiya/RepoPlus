from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class ReadProductModel(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    old_price: Optional[float]
    image_base64: Optional[str]  # Изменил на base64
    is_available: bool
    rating: Optional[int]
    reviews_count: int
    created_at: datetime

    class Config:
        from_attributes = True