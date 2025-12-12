from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.secure.jwt_helper import jwt_use
from app.settings.redis import redis
security = HTTPBearer()


async def get_auth_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        token = credentials.credentials
        
        # Проверяем, что токен не пустой
        if not token:
            raise credentials_exception
            
        # Декодируем JWT токен
        try:
            payload = jwt_use.decode_jwt(token)
        except Exception as jwt_error:
            raise HTTPException(
                status_code=401,
                detail=f"Invalid token: {str(jwt_error)}",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        id = payload.get('id')
        session_id = payload.get("session_id")
        
        if session_id is None or id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"}
            )
            
        # Проверяем токен в Redis
        redis_key = f"jwt_user_id:{str(id)}_session_id:{str(session_id)}"
        
        try:
            redis_token = await redis.get(redis_key)
        except Exception as e:
            print(f"❌ Redis error: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Redis connection error: {e}",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        if redis_token is None:
            raise HTTPException(
                status_code=401,
                detail="Token not found in redis",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Получаем данные из payload токена
        email: str = payload.get("email")
        name: str = payload.get("name")
        lastname: str = payload.get("lastname")

        result = {
            "id": id,
            "email": email,
            "name": name,
            "lastname": lastname
        }

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Authentication error: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
        