import random
from typing import Optional
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.repository.repo import AbstractRepo
from app.schemas.registers import RegisterSchema
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

    async def register(self,data:RegisterSchema)-> Optional[JSONResponse | HTTPException]:
        try:    
            name =  await self.user_repo.get_one(username = data.username)
            phone =  await self.user_repo.get_one(phone = data.phone)
            email =  await self.user_repo.get_one(email = data.email)
            print(name, phone,email)
            if name or phone or email :
                raise HTTPException(
                    status_code=409,
                    detail="Пользователь с такими данными уже существует!"
                )
            user_dict = data.model_dump()
            user_dict['password'] = self.jwt.hash_password(user_dict['password']).decode('utf-8')
            result = await self.user_repo.add_one(user_dict)
            print(result)
            if result:
                return HTTPException(
                    status_code=200,
                    detail="Ахуеть махуеть все норм"
                )
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=500)

    async def sendcode(self, id:int)->Optional[JSONResponse | HTTPException]:
        try:
            code = random.randint(10000,999999)
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
            await redis.set(name = f"verify_email:{user.email}", value=code,ex=120)
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
        

    async def verify_code(self, data:VerifyCode)->Optional[JSONResponse | HTTPException]:
        try:
            storage_code = await redis.get(f"verify_email:{data.email}")
            if storage_code is None:
                raise HTTPException(
                    status_code=404,
                    detail="Код не был отправлен"
                    )
            input_code = str(data.code)

            if storage_code.decode('utf-8') != input_code:
                raise HTTPException(
                    status_code=400,
                    detail="Не правильный код"
                )
            
            await self.user_repo.edit_one({'is_verified' : True}, email = data.email)
            await redis.delete(f"verify_email:{data.email}")
            return JSONResponse(
                status_code=200,
                content={"message": "Пользователь подтвержден!"}
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"{e}"
            )
