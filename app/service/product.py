import os
import uuid
from typing import List, Optional
from fastapi import HTTPException, UploadFile
from app.repository.repo import AbstractRepo
from app.schemas.product_create import CreateProductModel


class ProductService:
    def __init__(self, repository: AbstractRepo, jwt):
        self.product_repo = repository()
        self.jwt = jwt

    async def get_products(
        self, 
        offset: int = 0, 
        limit: int = 10,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        available: Optional[bool] = None
    ):
        try:
            # Строим фильтры
            filters = {}
            if available is not None:
                filters['is_available'] = available
            
            # Получаем товары из репозитория
            all_products = await self.product_repo.get_all(filters=filters)
            
            # Фильтруем по цене
            filtered_products = all_products
            if min_price is not None:
                filtered_products = [p for p in filtered_products if p.price >= min_price]
            if max_price is not None:
                filtered_products = [p for p in filtered_products if p.price <= max_price]
            
            # Применяем пагинацию
            paginated_products = filtered_products[offset:offset + limit]
            
            return paginated_products
            
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=500)

    async def get_product_by_id(self, product_id: int):
        try:
            product = await self.product_repo.get_one(id=product_id)
            if product is None:
                raise HTTPException(
                    status_code=404,
                    detail="Товар не найден"
                )
            
            return product.to_read_model()
            
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=500)

    async def search_products(self, query: str, offset: int = 0, limit: int = 10):
        try:
            # Получаем все товары
            all_products = await self.product_repo.get_all()
            
            # Поиск по названию (регистронезависимый)
            search_results = [
                p for p in all_products 
                if query.lower() in p.name.lower()
            ]
            
            # Применяем пагинацию
            paginated_results = search_results[offset:offset + limit]
            
            return paginated_results
            
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=500)

    async def create_product(self, data: CreateProductModel):
        try:
            product_dict = data.model_dump()
            result = await self.product_repo.add_one(product_dict)
            
            if result:
                # Получаем созданный товар
                created_product = await self.product_repo.get_one(id=result)
                return created_product.to_read_model()
            else:
                raise HTTPException(
                    status_code=500,
                    detail="Ошибка при создании товара"
                )
                
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=500)

    async def update_product(self, product_id: int, data: CreateProductModel):
        try:
            # Проверяем, существует ли товар
            existing_product = await self.product_repo.get_one(id=product_id)
            if existing_product is None:
                raise HTTPException(
                    status_code=404,
                    detail="Товар не найден"
                )
            
            # Обновляем товар
            product_dict = data.model_dump()
            updated_product = await self.product_repo.edit_one(product_dict, id=product_id)
            
            if updated_product:
                return updated_product.to_read_model()
            else:
                raise HTTPException(
                    status_code=500,
                    detail="Ошибка при обновлении товара"
                )
                
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=500)
    async def upload_image(self, product_id: int, file: UploadFile):
        try:
            # Проверяем, существует ли товар
            product = await self.product_repo.get_one(id=product_id)
            if product is None:
                raise HTTPException(
                    status_code=404,
                    detail="Товар не найден"
                )
            
            # Проверяем тип файла
            if not file.content_type.startswith('image/'):
                raise HTTPException(
                    status_code=400,
                    detail="Файл должен быть изображением"
                )
            
            # Создаем папку для изображений, если её нет
            media_dir = "media/products"
            os.makedirs(media_dir, exist_ok=True)
            
            # Генерируем уникальное имя файла
            file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
            filename = f"product_{product_id}_{uuid.uuid4().hex[:8]}.{file_extension}"
            file_path = os.path.join(media_dir, filename)
            
            # Сохраняем файл
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            # Обновляем товар с новым именем файла
            await self.product_repo.edit_one({"image_filename": filename}, id=product_id)
            
            return {"filename": filename, "message": "Изображение успешно загружено"}
            
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=500)