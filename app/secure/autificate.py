from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.secure.jwt_helper import jwt_use
from app.settings.redis import redis
oauth_shemes = OAuth2PasswordBearer(tokenUrl="/v2/users/signin/token-username/")


async def get_auth_user(token:str = Depends(oauth_shemes)):
    credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt_use.decode_jwt(token)
        id = payload.get('id')
        session_id = payload.get("session_id")
        if session_id is None or id is None:
            raise credentials_exception
        redis_token =  redis.get(name = f"jwt_user_id:{str(id)}_session_id:{str(session_id)}")
        if redis_token is None:
            raise HTTPException(
                status_code=401,
                detail="Not found in redis",
                eaders={"WWW-Authenticate": "Bearer"}
        )
        phone: str = payload.get("phone")
        email: str = payload.get("email")
        username: str = payload.get("username")
        role: str = payload.get("role")

        result = {
            "id": id,
            "username": username,
            "email": email,
            "phone": phone,
            "session_id": session_id,
            "role": role
        }

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
        