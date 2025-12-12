from pydantic import BaseModel, Field
from typing import Optional


class CreateCartItemModel(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(1, gt=0)
    
    # Настройки размера
    size_type: Optional[str] = Field(None, max_length=50)
    size_price_modifier: float = Field(0.0, ge=0)
    
    # Настройки кофе
    coffee_type: Optional[str] = Field(None, max_length=50)
    coffee_shots: int = Field(0, ge=0)
    coffee_price_modifier: float = Field(0.0, ge=0)
    
    # Настройки молока
    milk_type: Optional[str] = Field(None, max_length=50)
    milk_price_modifier: float = Field(0.0, ge=0)
    
    # Настройки сиропа
    syrup_type: Optional[str] = Field(None, max_length=50)
    syrup_price_modifier: float = Field(0.0, ge=0)

    class Config:
        from_attributes = True