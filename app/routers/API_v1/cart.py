import logging
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, List

from app.routers.dependecies import cart_service
from app.service.cart import CartService
from app.schemas.cart_create import CreateCartItemModel
from app.schemas.ReadORM.read_cart import ReadCartItemModel
from app.schemas.cart_response import CartResponseModel
from app.secure.autificate import get_auth_user

router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)
log = logging.getLogger("__name__")


@router.post("/add", response_model=ReadCartItemModel)
async def add_to_cart(
    service: Annotated[CartService, Depends(cart_service)],
    data: CreateCartItemModel,
    user_data: dict = Depends(get_auth_user)
):
    """
    ## Добавить товар в корзину
    
    Добавляет товар с кастомизацией в корзину пользователя.
    
    **Требует авторизации** (Bearer токен)
    
    **Кастомизация напитка:**
    - Размер: size_type + size_price_modifier
    - Кофе: coffee_type + coffee_shots + coffee_price_modifier  
    - Молоко: milk_type + milk_price_modifier
    - Сироп: syrup_type + syrup_price_modifier
    
    **Автоматический расчет цены:**
    total_price = (базовая_цена + все_модификаторы) × количество
    
    **Проверки:**
    - Товар существует и доступен
    - Пользователь авторизован
    """
    
    user_id = user_data["id"]
    result = await service.add_to_cart(user_id, data)
    return result


@router.get("/", response_model=CartResponseModel)
async def get_cart(
    service: Annotated[CartService, Depends(cart_service)],
    user_data: dict = Depends(get_auth_user)
):
    """Получить корзину пользователя с итогами"""
    
    user_id = user_data["id"]
    result = await service.get_cart(user_id)
    return result


@router.put("/{cart_item_id}", response_model=ReadCartItemModel)
async def update_cart_item(
    cart_item_id: int,
    quantity: int,
    service: Annotated[CartService, Depends(cart_service)],
    user_data: dict = Depends(get_auth_user)
):
    """Обновить количество товара в корзине"""
    
    user_id = user_data["id"]
    result = await service.update_quantity(user_id, cart_item_id, quantity)
    return result


@router.delete("/{cart_item_id}")
async def remove_from_cart(
    cart_item_id: int,
    service: Annotated[CartService, Depends(cart_service)],
    user_data: dict = Depends(get_auth_user)
):
    """Удалить позицию из корзины"""
    
    user_id = user_data["id"]
    result = await service.remove_from_cart(user_id, cart_item_id)
    return result


@router.delete("/clear")
async def clear_cart(
    service: Annotated[CartService, Depends(cart_service)],
    user_data: dict = Depends(get_auth_user)
):
    """Очистить всю корзину"""
    
    user_id = user_data["id"]
    result = await service.clear_cart(user_id)
    return result


