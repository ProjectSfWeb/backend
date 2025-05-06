from datetime import datetime, timedelta
from typing import Optional
from fastapi import Request

from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
from models import User

from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Создание токена пользователя

    :param data: Словарь с id пользователя для генерации токена
    :param expires_delta: Время существования токена
    :return: Токен пользователя
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=60))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    """
    Проверка токена на валидность

    :param token: Токен
    :param credentials_exception:
    :return: id пользователя с валидным токеном
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception


def get_token(request: Request):
    """
    Берет токен из браузера
    :param request: Запрос токена
    :return: возвращает токен пользователя
    """
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    return token


def get_current_user(token: str = Depends(get_token), db: Session = Depends(get_db)) -> User:
    """
    Возвращает текущего авторизованного пользователя

    :param token:
    :param db: Синхронная сессия для работы с бд
    :return: Возвращает авторизованного пользователя
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_id = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user