from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any, Self
from datetime import datetime, date


class TransactionCreate(BaseModel):
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
        if not(v.startswith("+7") or v.startswith("8")):
            raise ValueError("Некорректный формат номера")
        return v


    @field_validator("rec_inn")
    def validate_rec_inn(cls, v):
        if not(len(v) == 12):
            raise ValueError("Некорректный формат ИНН")
        return v


class TransactionUpdate(TransactionCreate):
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

    # @field_validator("timestamp")
    # def validate_date_format(cls, value):
    #     if value:
    #         try:
    #             return datetime.strptime(value, "%d.%m.%Y")
    #         except ValueError:
    #             raise ValueError("Дата должна быть в формате ДД.ММ.ГГГГ, например 01.01.2025")
    #     return value


class TransactionTypeSchema(BaseModel):
    id: int
    name: str


class CategorySchema(BaseModel):
    id: int
    name: str


class TransactionStatusSchema(BaseModel):
    id: int
    name: str


class PersonTypeSchema(BaseModel):
    id: int
    name: str


