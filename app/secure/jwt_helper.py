import uuid
from datetime import datetime, timedelta
import jwt
import bcrypt
from app.settings.db_settings import settings

# >>> private_key = b"-----BEGIN PRIVATE KEY-----\nMIGEAgEAMBAGByqGSM49AgEGBS..."
# >>> public_key = b"-----BEGIN PUBLIC KEY-----\nMHYwEAYHKoZIzj0CAQYFK4EEAC..."

class Jwt():

    def encode_jwt(
        self,
        payload: dict,
        access: bool,
        session_id:str,
        private_key: str = settings.jwt_config.PRIVATE_KEY_PATH.read_text(),
        algorithm: str = settings.jwt_config.ALGORITM,
        expire_minutes: int = settings.jwt_config.ACCESS_TOKEN_EXPIRE_IN_MINUTES,
        expire_days: int = settings.jwt_config.REFRESH_TOKEN_EXPIRE_IN_DAYS,
        expire_timedelta: timedelta | None = None,
    ) -> str:
        to_encode = payload.copy()
        now = datetime.utcnow()
        if expire_timedelta:
            expire = now + expire_timedelta
        elif access:
            expire = now + timedelta(minutes=expire_minutes)
        else:
            expire = now + timedelta(days=expire_days)
        to_encode.update(
            exp=expire,
            iat=now,
            session_id=session_id,
        )
        encoded = jwt.encode(
            to_encode,
            private_key,
            algorithm=algorithm,
        )
        return encoded


    def decode_jwt(
        self,
        token: str | bytes,
        public_key: str = settings.jwt_config.PUBLIC_KEY_PATH.read_text(),
        algorithm: str = settings.jwt_config.ALGORITM,
    ) -> dict:
        decoded = jwt.decode(
            token,
            public_key,
            algorithms=[algorithm],
        )
        return decoded


    def hash_password(
        self,
        password: str,
    ) -> bytes:
        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode()
        return bcrypt.hashpw(pwd_bytes, salt)


    def validate_password(
        self,
        password: str,
        hashed_password: bytes,
    ) -> bool:
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password,
        )
    

jwt_use = Jwt()