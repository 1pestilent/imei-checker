import bcrypt
from datetime import datetime, timedelta
import jwt

from app.core import config
from app.users import schemas

def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)

def verify_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)


def encode_jwt(
        payload: dict,
        private_key: str= config.PRIVATE_KEY_PATH.read_text(),
        algorithm: str = config.ALGORITHM,
        expire_minutes: int = config.ACCESS_TOKEN_EXPIRE_MINUTES,
        expire_timedelta: timedelta | None = None
        ):
    
    to_encode = payload.copy()
    now = datetime.utcnow()

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(
        iat = now,
        exp = expire
    )

    encoded = jwt.encode(to_encode, private_key, algorithm)
    return encoded

def decode_jwt(token: str | bytes, public_key: str = config.PUBLIC_KEY_PATH.read_text(), algorithm: str = config.ALGORITHM):
    decoded = jwt.decode(token,
                         public_key,
                         algorithms=[algorithm])
    return decoded