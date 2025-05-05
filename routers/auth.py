from fastapi import APIRouter, Depends, status, HTTPException
from fastapi import Response
from sqlalchemy.orm import Session

from schemas.user import UserCreate, UserLogin, UserResponse
from services.auth import register_user, login_user
from database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED,
             response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Регистрирует нового пользователя.
    Хеширует пароль и записывает данные в БД.
    """
    return register_user(db=db, user=user_data)


@router.post("/login")
def login(response: Response, user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Авторизует пользователя.
    Проверяет логин/пароль и возвращает access-токен.
    """
    token = login_user(db=db, user_data=user_data)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax"
    )
    if not token:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    return {"message": "Login successful"}
