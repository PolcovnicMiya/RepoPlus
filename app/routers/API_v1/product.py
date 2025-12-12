import logging
from fastapi import APIRouter, Query, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from typing import Optional, List, Annotated
import os

from app.routers.dependecies import product_service
from app.service.product import ProductService
from app.schemas.product_create import CreateProductModel
from app.schemas.ReadORM.read_product import ReadProductModel

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)
log = logging.getLogger("__name__")


@router.get("/", response_model=List[ReadProductModel])
async def get_products(
    service: Annotated[ProductService, Depends(product_service)],
    offset: int = Query(0, ge=0, description="Начальная позиция для пагинации"),
    limit: int = Query(10, ge=1, le=100, description="Количество товаров на странице (макс. 100)"),
    min_price: Optional[float] = Query(None, ge=0, description="Минимальная цена товара в тенге"),
    max_price: Optional[float] = Query(None, ge=0, description="Максимальная цена товара в тенге"),
    available: Optional[bool] = Query(None, description="Фильтр по доступности (true - только доступные)")
):
    """
    ## Получить список товаров кофейни
    
    Возвращает список всех товаров с возможностью фильтрации и пагинации.
    
    **Фильтры:**
    - По цене: min_price и max_price
    - По доступности: available (true/false)
    
    **Пагинация:**
    - offset: с какого элемента начать (0, 10, 20...)
    - limit: сколько элементов вернуть (макс. 100)
    
    **Изображения:**
    Поле `image_base64` содержит изображение товара в формате base64.
    """
    
    result = await service.get_products(
        offset=offset,
        limit=limit,
        min_price=min_price,
        max_price=max_price,
        available=available
    )
    return result


@router.get("/{product_id}", response_model=ReadProductModel)
async def get_product(
    product_id: int,
    service: Annotated[ProductService, Depends(product_service)]
):
    """
    ## Получить товар по ID
    
    Возвращает подробную информацию о конкретном товаре.
    
    **Включает:**
    - Название и описание товара
    - Цену (базовую и старую для скидок)
    - Изображение в формате base64
    - Рейтинг и количество отзывов
    - Статус доступности
    """
    
    result = await service.get_product_by_id(product_id)
    return result


@router.get("/search/", response_model=List[ReadProductModel])
async def search_products(
    service: Annotated[ProductService, Depends(product_service)],
    q: str = Query(..., min_length=1, description="Поисковый запрос (название товара)"),
    offset: int = Query(0, ge=0, description="Начальная позиция для пагинации"),
    limit: int = Query(10, ge=1, le=100, description="Количество товаров на странице")
):
    """
    ## Поиск товаров по названию
    
    Выполняет поиск товаров по названию (регистронезависимый).
    
    **Параметры:**
    - q: поисковый запрос (минимум 1 символ)
    - Поддерживает частичное совпадение
    - Регистр не учитывается
    
    **Примеры запросов:**
    - "латте" - найдет все товары с "латте" в названии
    - "кофе" - найдет все кофейные напитки
    - "чай" - найдет все чайные напитки
    """
    
    result = await service.search_products(
        query=q,
        offset=offset,
        limit=limit
    )
    return result


@router.post("/", response_model=ReadProductModel)
async def create_product(
    service: Annotated[ProductService, Depends(product_service)],
    data: CreateProductModel
):
    """
    ## Создать новый товар (Админ)
    
    Создает новый товар в каталоге кофейни.
    
    **Обязательные поля:**
    - name: название товара
    - price: цена в тенге
    
    **Опциональные поля:**
    - description: описание товара
    - old_price: старая цена для отображения скидки
    - image_filename: имя файла изображения
    - is_available: доступность (по умолчанию true)
    - rating: рейтинг в процентах (0-100)
    - reviews_count: количество отзывов
    """
    
    result = await service.create_product(data)
    return result


@router.put("/{product_id}", response_model=ReadProductModel)
async def update_product(
    product_id: int,
    service: Annotated[ProductService, Depends(product_service)],
    data: CreateProductModel
):
    """
    ## Обновить товар (Админ)
    
    Обновляет существующий товар в каталоге.
    
    **Можно изменить:**
    - Название и описание
    - Цену (базовую и старую)
    - Доступность товара
    - Рейтинг и количество отзывов
    - Имя файла изображения
    
    **Примечание:** Для загрузки нового изображения используйте отдельную ручку upload-image
    """
    
    result = await service.update_product(product_id, data)
    return result

@router.post("/{product_id}/upload-image")
async def upload_product_image(
    product_id: int,
    service: Annotated[ProductService, Depends(product_service)],
    file: UploadFile = File(...)
):
    """
    ## Загрузить изображение для товара (Админ)
    
    Загружает изображение для существующего товара.
    
    **Поддерживаемые форматы:**
    - JPG, JPEG, PNG, WEBP
    - Максимальный размер: не ограничен
    
    **Процесс:**
    1. Проверяет существование товара
    2. Валидирует тип файла (только изображения)
    3. Генерирует уникальное имя файла
    4. Сохраняет в папку media/products/
    5. Обновляет поле image_filename в базе данных
    
    **Возвращает:** имя сохраненного файла и сообщение об успехе
    """
    
    result = await service.upload_image(product_id, file)
    return result


@router.get("/media/{filename}")
async def get_product_image(filename: str):
    """
    ## Получить изображение товара
    
    Возвращает файл изображения по имени файла.
    
    **Использование:**
    - Прямая ссылка на изображение товара
    - Используется для отображения картинок в каталоге
    
    **Примечание:** 
    В API товаров изображения возвращаются в base64 формате,
    эта ручка нужна для прямого доступа к файлам.
    
    **Пример:** `/v1/products/media/product_1_abc123.jpg`
    """
    
    file_path = os.path.join("media/products", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Изображение не найдено")
    
    return FileResponse(file_path)