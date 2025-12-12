import random
from typing import Optional
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.repository.repo import AbstractRepo
from app.schemas.user_create import CreateUserModel
from app.schemas.register_response import RegisterResponseModel
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.settings.db_settings import settings
from app.settings.redis import redis
from app.schemas.verify import VerifyCode


class RegisterService:
    def __init__(self, repository:AbstractRepo, jwt):
        self.user_repo = repository()
        self.jwt = jwt

    async def register(self, data: CreateUserModel) -> RegisterResponseModel:
        try:    
            # Проверяем, существует ли пользователь с такой почтой
            existing_user = await self.user_repo.get_one(email=data.email)
            if existing_user:
                raise HTTPException(
                    status_code=409,
                    detail="Пользователь с такой почтой уже существует!"
                )
            
            # Подготавливаем данные для создания пользователя
            user_dict = data.model_dump()
            user_dict['password'] = self.jwt.hash_password(user_dict['password']).decode('utf-8')
            
            # Создаем пользователя и получаем его ID
            user_id = await self.user_repo.add_one(user_dict)
            
            if user_id:
                return RegisterResponseModel(user_id=user_id)
            else:
                raise HTTPException(
                    status_code=500,
                    detail="Ошибка при создании пользователя"
                )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=500)

    async def sendcode(self, id:int)->Optional[JSONResponse | HTTPException]:
        try:
            code = random.randint(100000,999999)
            user = await self.user_repo.get_one(id = id)
            if user is None:
                raise HTTPException (
                    status_code=404,
                    detail="Такого пользователя не существует"
                )
            if user.is_verified:
                raise HTTPException(
                    status_code=400,
                    detail = "Пользователь уже верифицирован"
                )
            await redis.set(name = f"verify_email:{user.email}", value=code,ex=180)
            message = MIMEMultipart()
            message['FROM'] = settings.smtp.SMTP_EMAIL
            message['TO'] = user.email
            message['Subject'] = "Your verification code"
            message.attach(MIMEText(str(code),"plain"))
            server = smtplib.SMTP(settings.smtp.SMTP_HOST,settings.smtp.SMTP_PORT)
            server.starttls()
            server.login(settings.smtp.SMTP_EMAIL, settings.smtp.SMTP_EMAILPASSWOR)
            server.send_message(message)
            server.quit()


            return JSONResponse(
                status_code=200,
                content={"content": f"Nice bro vot code:{code}"}
            )
            

        except Exception as e:
              raise HTTPException(
                  status_code=500,
                  detail=f"{e}"
              )
        

    async def verify_code(self, data: VerifyCode) -> Optional[JSONResponse | HTTPException]:
        try:
            # Получаем пользователя по ID
            user = await self.user_repo.get_one(id=data.user_id)
            if user is None:
                raise HTTPException(
                    status_code=404,
                    detail="Пользователь не найден"
                )
            
            # Проверяем код в Redis по email пользователя
            storage_code = await redis.get(f"verify_email:{user.email}")
            if storage_code is None:
                raise HTTPException(
                    status_code=404,
                    detail="Код не был отправлен"
                )
            
            input_code = str(data.code)
            if storage_code.decode('utf-8') != input_code:
                raise HTTPException(
                    status_code=400,
                    detail="Неправильный код"
                )
            
            # Обновляем статус верификации пользователя
            await self.user_repo.edit_one({'is_verified': True}, id=data.user_id)
            await redis.delete(f"verify_email:{user.email}")
            
            return JSONResponse(
                status_code=200,
                content={"message": "Пользователь подтвержден!"}
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"{e}"
            )
