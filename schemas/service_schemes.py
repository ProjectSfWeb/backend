from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any, Self
from datetime import datetime, date


class TransactionCreate(BaseModel):
    """
    Схема для создания новой транзакции
    """
    transTypeID: int
    category_name: str
    amount: int
    comment: Optional[str] = None
    person_typeID: int
    sender_bank: str
    receiver_bank: str
    account: str
    rec_inn: str
    rec_acc: str
    rec_phone: str


    @field_validator("rec_phone")
    def validate_rec_phone(cls, v):
        """
        Валидатор номера телефона
        """
        if not(v.startswith("+7") or v.startswith("8")):
            raise ValueError("Некорректный формат номера")
        return v


    @field_validator("rec_inn")
    def validate_rec_inn(cls, v):
        """
        Валидатор ИНН
        """
        if not(len(v) == 12):
            raise ValueError("Некорректный формат ИНН")
        return v


class TransactionUpdate(TransactionCreate):
    """
    Схема для обновления транзакции
    """
    person_typeID: Optional[int]
    timestamp: Optional[date]
    comment: Optional[str]
    amount: Optional[int]
    status_id: Optional[int]
    sender_bank: Optional[str]
    receiver_bank: Optional[str]
    rec_inn: Optional[str]
    category_name: Optional[str]
    rec_phone: Optional[str]



class TransactionTypeSchema(BaseModel):
    """
    Схема типа транзакции
    """
    id: int
    name: str


class CategorySchema(BaseModel):
    """
    Схема категорий транзакции
    """
    id: int
    name: str


class TransactionStatusSchema(BaseModel):
    """
    Схема статуса транзакции
    """
    id: int
    name: str


class PersonTypeSchema(BaseModel):
    """
    Схема типа лица
    """
    id: int
    name: str


