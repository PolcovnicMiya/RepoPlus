from typing import List
from fastapi import HTTPException
from app.repository.repo import AbstractRepo
from app.schemas.cart_create import CreateCartItemModel


class CartService:
    def __init__(self, repository: AbstractRepo, jwt):
        self.cart_repo = repository()
        self.jwt = jwt

    async def add_to_cart(self, user_id: int, data: CreateCartItemModel):
        try:
            # Проверяем, существует ли товар
            from app.repository.product import product_repo
            product = await product_repo.get_one(id=data.product_id)
            if product is None:
                raise HTTPException(
                    status_code=404,
                    detail="Товар не найден"
                )
            
            # Проверяем, доступен ли товар
            if not product.is_available:
                raise HTTPException(
                    status_code=400,
                    detail="Товар недоступен"
                )
            
            # Рассчитываем итоговую цену
            base_price = float(product.price)
            total_modifiers = (
                data.size_price_modifier + 
                data.coffee_price_modifier + 
                data.milk_price_modifier + 
                data.syrup_price_modifier
            )
            total_price = (base_price + total_modifiers) * data.quantity
            
            # Подготавливаем данные для сохранения
            cart_data = data.model_dump()
            cart_data['user_id'] = user_id
            cart_data['total_price'] = total_price
            
            # Сохраняем в корзину
            cart_item_id = await self.cart_repo.add_one(cart_data)
            
            if cart_item_id:
                # Получаем созданную позицию
                created_item = await self.cart_repo.get_one(id=cart_item_id)
                return created_item.to_read_model()
            else:
                raise HTTPException(
                    status_code=500,
                    detail="Ошибка при добавлении в корзину"
                )
                
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=500)

    async def get_cart(self, user_id: int):
        try:
            # Получаем все позиции корзины пользователя
            cart_items = await self.cart_repo.get_all(filters={'user_id': user_id})
            
            # Рассчитываем итоги
            total_items = len(cart_items)
            total_amount = sum(item.total_price for item in cart_items)
            discount = 0.0  # пока без скидок
            final_amount = total_amount - discount
            
            # Формируем ответ
            from app.schemas.cart_response import CartResponseModel, CartSummaryModel
            
            summary = CartSummaryModel(
                total_items=total_items,
                total_amount=total_amount,
                discount=discount,
                final_amount=final_amount
            )
            
            return CartResponseModel(
                items=cart_items,
                summary=summary
            )
            
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=500)

    async def update_quantity(self, user_id: int, cart_item_id: int, quantity: int):
        try:
            # Проверяем, что позиция принадлежит пользователю
            cart_item = await self.cart_repo.get_one(id=cart_item_id, user_id=user_id)
            if cart_item is None:
                raise HTTPException(
                    status_code=404,
                    detail="Позиция в корзине не найдена"
                )
            
            # Проверяем корректность количества
            if quantity <= 0:
                raise HTTPException(
                    status_code=400,
                    detail="Количество должно быть больше 0"
                )
            
            # Получаем товар для пересчета цены
            from app.repository.product import product_repo
            product = await product_repo.get_one(id=cart_item.product_id)
            
            # Пересчитываем цену
            base_price = float(product.price)
            total_modifiers = (
                cart_item.size_price_modifier + 
                cart_item.coffee_price_modifier + 
                cart_item.milk_price_modifier + 
                cart_item.syrup_price_modifier
            )
            new_total_price = (base_price + total_modifiers) * quantity
            
            # Обновляем позицию
            updated_item = await self.cart_repo.edit_one(
                {'quantity': quantity, 'total_price': new_total_price}, 
                id=cart_item_id
            )
            
            if updated_item:
                return updated_item.to_read_model()
            else:
                raise HTTPException(
                    status_code=500,
                    detail="Ошибка при обновлении корзины"
                )
                
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=500)

    async def remove_from_cart(self, user_id: int, cart_item_id: int):
        try:
            # Проверяем, что позиция принадлежит пользователю
            cart_item = await self.cart_repo.get_one(id=cart_item_id, user_id=user_id)
            if cart_item is None:
                raise HTTPException(
                    status_code=404,
                    detail="Позиция в корзине не найдена"
                )
            
            # Удаляем позицию
            deleted = await self.cart_repo.delete_one(id=cart_item_id)
            
            if deleted:
                return {"message": "Позиция удалена из корзины"}
            else:
                raise HTTPException(
                    status_code=500,
                    detail="Ошибка при удалении из корзины"
                )
                
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=500)

    async def clear_cart(self, user_id: int):
        try:
            # Получаем все позиции пользователя
            cart_items = await self.cart_repo.get_all(filters={'user_id': user_id})
            
            # Удаляем каждую позицию
            deleted_count = 0
            for item in cart_items:
                deleted = await self.cart_repo.delete_one(id=item.id)
                if deleted:
                    deleted_count += 1
            
            return {"message": f"Удалено {deleted_count} позиций из корзины"}
                
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=500)

