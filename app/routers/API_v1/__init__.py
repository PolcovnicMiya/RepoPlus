from fastapi import APIRouter
from .user import router as user_router
from .product import router as product_router
from .cart import router as cart_router
from .admin import router as admin_router

router = APIRouter(
    prefix="/v1"
)
router.include_router(user_router)
router.include_router(product_router)
router.include_router(cart_router)
router.include_router(admin_router)