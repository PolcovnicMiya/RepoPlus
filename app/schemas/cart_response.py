from pydantic import BaseModel
from typing import List
from app.schemas.ReadORM.read_cart import ReadCartItemModel


class CartSummaryModel(BaseModel):
    total_items: int  # общее количество позиций
    total_amount: float  # общая сумма
    discount: float = 0.0  # скидка (пока 0)
    final_amount: float  # итого к оплате

    class Config:
        from_attributes = True


class CartResponseModel(BaseModel):
    items: List[ReadCartItemModel]  # позиции в корзине
    summary: CartSummaryModel  # итоги

    class Config:
        from_attributes = True