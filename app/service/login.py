from datetime import datetime, timedelta
from typing import Optional
import uuid
from fastapi import HTTPException
from app.repository.repo import AbstractRepo
from app.secure.jwt_helper import Jwt
from app.settings.db_settings import settings
from app.settings.redis import redis

class LoginService:
    def __init__(self, user_repo:AbstractRepo, jwt):
        self.user_repo = user_repo()
        self.jwt = jwt


    async def _get_user_to_username(self, username : str):
        user =  await self.user_repo.get_one(username = username)
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="Пользователь с указанным username не найден!"
            )
        return user
    
    async def _get_user_by_email(self, email: str):
        user = await self.user_repo.get_one(email=email)
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="Пользователь с указанной почтой не найден!"
            )
        return user
    

    async def login_by_username(self, data):
        try:    
            user = await self._get_user_to_username(username=data.username)
            if not self.jwt.validate_password(password = data.password,hashed_password=user.password.encode('utf-8')):
                raise HTTPException(
                    status_code=400,
                    detail="Неверный пароль!"
                )
            session_id=str(uuid.uuid4())
            
            access_token = self.jwt.encode_jwt(payload = {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role
                    },
                    access = True,
                    session_id = session_id,)
            refresh_token = self.jwt.encode_jwt(payload = {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role
                    },
                    access = False,
                    session_id = session_id,)

            await redis.set(name = f"jwt_user_id:{str(user.id)}_session_id:{str(session_id)}",
                                        value = access_token, 
                                        ex = settings.jwt_config.ACCESS_TOKEN_EXPIRE_IN_MINUTES) 
            
            await redis.set(name = f"jwt_refresh_user_id:{str(user.id)}_session_id:{str(session_id)}",
                                        value = refresh_token, 
                                        ex = settings.jwt_config.REFRESH_TOKEN_EXPIRE_IN_DAYS * 24 * 60) 
            
            return{"access_token": access_token, "refresh_token": refresh_token}
            
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=500)

    async def login_by_email(self, email: str, password: str):
        try:    
            user = await self._get_user_by_email(email=email)
            
            # Проверяем, верифицирован ли пользователь
            if not user.is_verified:
                raise HTTPException(
                    status_code=403,
                    detail="Пользователь не верифицирован! Подтвердите email."
                )
            
            # Проверяем пароль
            if not self.jwt.validate_password(password=password, hashed_password=user.password.encode('utf-8')):
                raise HTTPException(
                    status_code=400,
                    detail="Неверный пароль!"
                )
            
            session_id = str(uuid.uuid4())
            
            # Создаем payload для токена
            payload = {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "lastname": user.lastname
            }
            
            access_token = self.jwt.encode_jwt(
                payload=payload,
                access=True,
                session_id=session_id
            )
            
            refresh_token = self.jwt.encode_jwt(
                payload=payload,
                access=False,
                session_id=session_id
            )

            # Сохраняем токены в Redis
            redis_key = f"jwt_user_id:{str(user.id)}_session_id:{str(session_id)}"
            
            try:
                await redis.set(
                    redis_key,
                    access_token, 
                    ex=settings.jwt_config.ACCESS_TOKEN_EXPIRE_IN_MINUTES
                )
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Redis error: {e}") 
            
            refresh_redis_key = f"jwt_refresh_user_id:{str(user.id)}_session_id:{str(session_id)}"
            await redis.set(
                refresh_redis_key,
                refresh_token, 
                ex=settings.jwt_config.REFRESH_TOKEN_EXPIRE_IN_DAYS * 24 * 60
            )
            
            # Проверяем, что токен действительно сохранился
            saved_token = await redis.get(redis_key)
            if not saved_token:
                raise HTTPException(status_code=500, detail="Failed to save token to Redis") 
            
            return {
                "access_token": access_token, 
                "refresh_token": refresh_token,
                "user_id": user.id
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=500)

    async def refresh_access_token(self, refresh_token: str):
        try:
            try:
                payload = self.jwt.decode_jwt(refresh_token)
            except Exception as jwt_error:
                raise HTTPException(
                    status_code=401,
                    detail=f"Invalid refresh token: {str(jwt_error)}"
                )
            
            user_id = payload.get('id')
            session_id = payload.get("session_id")
            
            if session_id is None or user_id is None:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid refresh token payload"
                )
            
            refresh_redis_key = f"jwt_refresh_user_id:{str(user_id)}_session_id:{str(session_id)}"
            
            try:
                stored_refresh_token = await redis.get(refresh_redis_key)
                if stored_refresh_token:
                    if isinstance(stored_refresh_token, bytes):
                        stored_refresh_token = stored_refresh_token.decode('utf-8')
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Redis connection error: {e}"
                )
            
            if stored_refresh_token is None:
                raise HTTPException(
                    status_code=401,
                    detail="Refresh token not found or expired"
                )
            
            if stored_refresh_token != refresh_token:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid refresh token"
                )
            
            user = await self.user_repo.get_one(id=user_id)
            if user is None:
                raise HTTPException(
                    status_code=404,
                    detail="User not found"
                )
            
            new_payload = {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "lastname": user.lastname
            }
            
            new_access_token = self.jwt.encode_jwt(
                payload=new_payload,
                access=True,
                session_id=session_id
            )
            
            access_redis_key = f"jwt_user_id:{str(user.id)}_session_id:{str(session_id)}"
            await redis.set(
                access_redis_key,
                new_access_token, 
                ex=settings.jwt_config.ACCESS_TOKEN_EXPIRE_IN_MINUTES
            )
            
            return {
                "access_token": new_access_token,
                "refresh_token": refresh_token
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=500)
    

        
    

