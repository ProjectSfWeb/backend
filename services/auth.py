from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models import User
from utils.jwt import create_access_token
from fastapi import HTTPException, status
from pydantic import EmailStr
from schemas.user import UserCreate, UserLogin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Хеширование пароля
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Проверка соответствия пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Регистрация пользователя
def register_user(db: Session, user: UserCreate):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    hashed_pw = hash_password(user.password)
    new_user = User(username=user.username, password_hash=hashed_pw,
                    email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Авторизация пользователя
def login_user(db: Session, user_data: UserLogin):
    user = db.query(User).filter(User.username == user_data.login).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Генерация токена
    token = create_access_token(data={"user_id": user.id})
    return token