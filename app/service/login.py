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
            
            await redis.set(name = f"jwt_user_id:{str(user.id)}_session_id:{str(session_id)}",
                                        value = refresh_token, 
                                        ex = settings.jwt_config.REFRESH_TOKEN_EXPIRE_IN_DAYS) 
            
            return{"access_token": access_token, "refresh_token": refresh_token}
            
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=500)
    

        
    

