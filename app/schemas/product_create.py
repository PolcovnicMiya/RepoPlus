from pydantic import BaseModel, Field
from typing import Optional


class CreateProductModel(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    price: float = Field(..., gt=0)
    old_price: Optional[float] = Field(None, gt=0)
    image_filename: Optional[str] = Field(None, max_length=255)
    is_available: bool = True
    rating: Optional[int] = Field(None, ge=0, le=100)
    reviews_count: int = Field(0, ge=0)

    class Config:
        from_attributes = True