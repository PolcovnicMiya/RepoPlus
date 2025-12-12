import random
from datetime import datetime, timedelta
from typing import List
from fastapi import HTTPException
from app.repository.user import user_repo
from app.repository.product import product_repo
from app.repository.cart import cart_repo
from app.secure.jwt_helper import jwt_use


class MockDataService:
    def __init__(self):
        self.user_repo = user_repo
        self.product_repo = product_repo
        self.cart_repo = cart_repo

    async def create_mock_users(self) -> List[dict]:
        """Создает 5 моковых пользователей"""
        mock_users = [
            {
                "name": "Алексей",
                "lastname": "Иванов",
                "email": "alexey.ivanov@example.com",
                "password": jwt_use.hash_password("password123").decode('utf-8'),
                "is_verified": True
            },
            {
                "name": "Мария",
                "lastname": "Петрова",
                "email": "maria.petrova@example.com",
                "password": jwt_use.hash_password("password123").decode('utf-8'),
                "is_verified": True
            },
            {
                "name": "Дмитрий",
                "lastname": "Сидоров",
                "email": "dmitry.sidorov@example.com",
                "password": jwt_use.hash_password("password123").decode('utf-8'),
                "is_verified": False
            },
            {
                "name": "Анна",
                "lastname": "Козлова",
                "email": "anna.kozlova@example.com",
                "password": jwt_use.hash_password("password123").decode('utf-8'),
                "is_verified": True
            },
            {
                "name": "Сергей",
                "lastname": "Морозов",
                "email": "sergey.morozov@example.com",
                "password": jwt_use.hash_password("password123").decode('utf-8'),
                "is_verified": True
            }
        ]
        
        created_users = []
        for user_data in mock_users:
            try:
                # Проверяем, существует ли пользователь с таким email
                existing_user = await self.user_repo.get_one(email=user_data["email"])
                if existing_user:
                    print(f"Пользователь с email {user_data['email']} уже существует")
                    created_users.append(existing_user)
                    continue
                    
                user = await self.user_repo.add_one(data=user_data)
                created_users.append(user)
                print(f"Создан пользователь: {user_data['name']} {user_data['lastname']}")
            except Exception as e:
                print(f"Ошибка создания пользователя {user_data['email']}: {e}")
                
        return created_users

    async def create_mock_products(self) -> List[dict]:
        """Создает 5 моковых продуктов"""
        mock_products = [
            {
                "name": "Эспрессо",
                "description": "Классический итальянский эспрессо с насыщенным вкусом и ароматом",
                "price": 150.00,
                "old_price": 180.00,
                "image_filename": "espresso.jpg",
                "is_available": True,
                "rating": 95,
                "reviews_count": 127
            },
            {
                "name": "Капучино",
                "description": "Нежный капучино с воздушной молочной пенкой и корицей",
                "price": 220.00,
                "old_price": None,
                "image_filename": "cappuccino.jpg",
                "is_available": True,
                "rating": 88,
                "reviews_count": 89
            },
            {
                "name": "Латте",
                "description": "Мягкий латте с большим количеством молока и красивым латте-артом",
                "price": 250.00,
                "old_price": 280.00,
                "image_filename": "latte.jpg",
                "is_available": True,
                "rating": 92,
                "reviews_count": 156
            },
            {
                "name": "Американо",
                "description": "Крепкий американо для тех, кто любит насыщенный кофейный вкус",
                "price": 180.00,
                "old_price": None,
                "image_filename": "americano.jpg",
                "is_available": False,
                "rating": 85,
                "reviews_count": 73
            },
            {
                "name": "Мокко",
                "description": "Сладкий мокко с шоколадным сиропом и взбитыми сливками",
                "price": 290.00,
                "old_price": 320.00,
                "image_filename": "mocha.jpg",
                "is_available": True,
                "rating": 90,
                "reviews_count": 112
            }
        ]
        
        created_products = []
        for product_data in mock_products:
            try:
                # Проверяем, существует ли продукт с таким названием
                existing_product = await self.product_repo.get_one(name=product_data["name"])
                if existing_product:
                    print(f"Продукт {product_data['name']} уже существует")
                    created_products.append(existing_product)
                    continue
                    
                product = await self.product_repo.add_one(data=product_data)
                created_products.append(product)
                print(f"Создан продукт: {product_data['name']}")
            except Exception as e:
                print(f"Ошибка создания продукта {product_data['name']}: {e}")
                
        return created_products

    async def create_mock_cart_items(self, users: List[dict], products: List[dict]) -> List[dict]:
        """Создает 5 моковых элементов корзины"""
        if not users or not products:
            raise HTTPException(status_code=400, detail="Нет пользователей или продуктов для создания корзины")
        
        # Варианты настроек для кофе
        size_options = [
            {"type": "small", "modifier": 0.0},
            {"type": "medium", "modifier": 20.0},
            {"type": "large", "modifier": 40.0}
        ]
        
        coffee_options = [
            {"type": "espresso_roast", "shots": 2, "modifier": 0.0},
            {"type": "decaf", "shots": 1, "modifier": 10.0},
            {"type": "double_shot", "shots": 4, "modifier": 30.0}
        ]
        
        milk_options = [
            {"type": "regular", "modifier": 0.0},
            {"type": "oat", "modifier": 25.0},
            {"type": "soy", "modifier": 20.0},
            {"type": "coconut", "modifier": 30.0}
        ]
        
        syrup_options = [
            {"type": "none", "modifier": 0.0},
            {"type": "caramel", "modifier": 35.0},
            {"type": "vanilla", "modifier": 30.0},
            {"type": "hazelnut", "modifier": 35.0}
        ]
        
        created_cart_items = []
        
        for i in range(5):
            user = random.choice(users)
            product = random.choice(products)
            size = random.choice(size_options)
            coffee = random.choice(coffee_options)
            milk = random.choice(milk_options)
            syrup = random.choice(syrup_options)
            quantity = random.randint(1, 3)
            
            # Рассчитываем итоговую цену
            # Проверяем, является ли product объектом или ID
            if hasattr(product, 'price'):
                base_price = float(product.price)
                user_id = user.id if hasattr(user, 'id') else user
                product_id = product.id if hasattr(product, 'id') else product
                product_name = product.name if hasattr(product, 'name') else f"Product {product_id}"
                user_name = user.name if hasattr(user, 'name') else f"User {user_id}"
            else:
                # Если это ID, получаем объект из БД
                product_obj = await self.product_repo.get_one(id=product)
                user_obj = await self.user_repo.get_one(id=user)
                if not product_obj or not user_obj:
                    continue
                base_price = float(product_obj.price)
                user_id = user_obj.id
                product_id = product_obj.id
                product_name = product_obj.name
                user_name = user_obj.name
            
            total_modifiers = size["modifier"] + coffee["modifier"] + milk["modifier"] + syrup["modifier"]
            total_price = (base_price + total_modifiers) * quantity
            
            cart_item_data = {
                "user_id": user_id,
                "product_id": product_id,
                "quantity": quantity,
                "size_type": size["type"],
                "size_price_modifier": size["modifier"],
                "coffee_type": coffee["type"],
                "coffee_shots": coffee["shots"],
                "coffee_price_modifier": coffee["modifier"],
                "milk_type": milk["type"],
                "milk_price_modifier": milk["modifier"],
                "syrup_type": syrup["type"],
                "syrup_price_modifier": syrup["modifier"],
                "total_price": total_price
            }
            
            try:
                cart_item = await self.cart_repo.add_one(data=cart_item_data)
                created_cart_items.append(cart_item)
                print(f"Создан элемент корзины: {product_name} для пользователя {user_name}")
            except Exception as e:
                print(f"Ошибка создания элемента корзины: {e}")
                
        return created_cart_items

    async def create_all_mock_data(self) -> dict:
        """Создает все моковые данные"""
        try:
            print("🚀 Начинаем создание моковых данных...")
            
            # Создаем пользователей
            print("👥 Создаем пользователей...")
            users = await self.create_mock_users()
            
            # Создаем продукты
            print("☕ Создаем продукты...")
            products = await self.create_mock_products()
            
            # Получаем все созданные объекты из БД для корзины
            print("🔍 Получаем созданные объекты из БД...")
            all_users = await self.user_repo.get_all()
            all_products = await self.product_repo.get_all()
            
            # Создаем элементы корзины
            print("🛒 Создаем элементы корзины...")
            cart_items = await self.create_mock_cart_items(all_users, all_products)
            
            result = {
                "users_created": len(users),
                "products_created": len(products),
                "cart_items_created": len(cart_items),
                "message": "Моковые данные успешно созданы!"
            }
            
            print("✅ Моковые данные созданы успешно!")
            return result
            
        except Exception as e:
            print(f"❌ Ошибка создания моковых данных: {e}")
            raise HTTPException(status_code=500, detail=f"Ошибка создания моковых данных: {str(e)}")


# Создаем экземпляр сервиса
mock_data_service = MockDataService()