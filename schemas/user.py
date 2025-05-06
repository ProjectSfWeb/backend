from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """
    Схема создания нового пользователя
    """
    username: str
    password: str
    email: EmailStr


class UserLogin(BaseModel):
    """
    Схема логина пользователя
    """
    login: str
    password: str


class UserResponse(BaseModel):
    """
    Схема пользователя для ответа фронту
    """
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True