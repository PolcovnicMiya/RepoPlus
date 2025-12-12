from fastapi import APIRouter, HTTPException
from app.service.mock_data import mock_data_service

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.post("/create-mock-data")
async def create_mock_data():
    try:
        result = await mock_data_service.create_all_mock_data()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create-mock-users")
async def create_mock_users():
    try:
        users = await mock_data_service.create_mock_users()
        return {
            "users_created": len(users),
            "message": f"Создано {len(users)} пользователей"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create-mock-products")
async def create_mock_products():
    try:
        products = await mock_data_service.create_mock_products()
        return {
            "products_created": len(products),
            "message": f"Создано {len(products)} продуктов"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create-mock-cart")
async def create_mock_cart():
    try:
        from app.repository.user import user_repo
        from app.repository.product import product_repo
        
        users = await user_repo.get_all()
        products = await product_repo.get_all()
        
        if not users:
            raise HTTPException(status_code=400, detail="Нет пользователей в БД. Сначала создайте пользователей.")
        
        if not products:
            raise HTTPException(status_code=400, detail="Нет продуктов в БД. Сначала создайте продукты.")
        
        cart_items = await mock_data_service.create_mock_cart_items(users, products)
        return {
            "cart_items_created": len(cart_items),
            "message": f"Создано {len(cart_items)} элементов корзины"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))