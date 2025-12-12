from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class ReadCartItemModel(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    size_type: Optional[str]
    size_price_modifier: float
    coffee_type: Optional[str]
    coffee_shots: int
    coffee_price_modifier: float
    milk_type: Optional[str]
    milk_price_modifier: float
    syrup_type: Optional[str]
    syrup_price_modifier: float
    total_price: float
    created_at: datetime

    class Config:
        from_attributes = True