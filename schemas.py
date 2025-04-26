from pydantic import BaseModel, Field, field_validator
from typing import Optional


class TransactionCreate(BaseModel):
    user_id: int
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