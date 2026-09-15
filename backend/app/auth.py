import os
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from jose import JWTError, jwt
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from app import db_models

SECRET_KEY = os.getenv('VOXMINDS_JWT_SECRET', 'dev-only-change-this-secret-to-a-long-random-value')
ENV = os.getenv('VOXMINDS_ENV', 'development').lower()
if ENV == 'production' and (SECRET_KEY.startswith('dev-only') or len(SECRET_KEY) < 32):
    raise RuntimeError('VOXMINDS_JWT_SECRET must be a long random secret in production')
ALGORITHM = 'HS256'
ACCESS_TTL_MINUTES = int(os.getenv('VOXMINDS_ACCESS_TTL_MINUTES', '15'))
REFRESH_TTL_DAYS = int(os.getenv('VOXMINDS_REFRESH_TTL_DAYS', '7'))
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, stored: str) -> bool:
    try:
        return password_hash.verify(password, stored)
    except Exception:
        return False


def _token(subject: int, token_type: str, expires: timedelta, jti: str | None = None) -> str:
    now = datetime.now(timezone.utc)
    payload = {'sub': str(subject), 'type': token_type, 'iat': now, 'exp': now + expires, 'jti': jti or str(uuid4())}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(user_id: int) -> str:
    return _token(user_id, 'access', timedelta(minutes=ACCESS_TTL_MINUTES))


def create_refresh_token(user_id: int) -> tuple[str, str, datetime]:
    jti = str(uuid4())
    expires = datetime.now(timezone.utc) + timedelta(days=REFRESH_TTL_DAYS)
    token = _token(user_id, 'refresh', timedelta(days=REFRESH_TTL_DAYS), jti)
    return token, jti, expires.replace(tzinfo=None)


def decode_token(token: str, expected_type: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get('type') != expected_type or not payload.get('sub'):
            return None
        return payload
    except JWTError:
        return None


def get_user_from_access_token(token: str, db: Session):
    payload = decode_token(token, 'access')
    if not payload:
        return None
    try:
        return db.get(db_models.User, int(payload['sub']))
    except (ValueError, TypeError):
        return None
