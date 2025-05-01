from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from datetime import datetime

from schemas import (TransactionCreate, TransactionTypeSchema, CategorySchema,
                     TransactionStatusSchema, PersonTypeSchema)

router = APIRouter(tags=["Transactions"])


@router.post("/transactions/", status_code=201)
def create_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db)
):
    """
    Роут для добавления транзакции.
    Принимает user_id, тип, категорию, сумму и комментарий.
    """
    try:
        # Проверка, есть ли такая категория уже
        category = db.query(models.Category).filter_by(name=data.category_name).first()
        if not category:
            # Если нет — создаём новую
            category = models.Category(name=data.category_name)
            db.add(category)
            db.commit()
            db.refresh(category)

        # Создаём объект транзакции
        transaction = models.Transaction(
            user_id=data.user_id,
            transTypeID=data.transTypeID,
            category_id=category.id,
            amount=data.amount,
            comment=data.comment,
            timestamp=datetime.utcnow(),
            status_id=1,  # по умолчанию статус
            person_typeID=data.person_typeID,
            sender_bank=data.sender_bank,
            receiver_bank=data.receiver_bank,
            account=data.account,
            rec_inn=data.rec_inn,
            rec_acc=data.rec_acc,
            rec_phone=data.rec_phone

        )

        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return {"status": "success", "transaction_id": transaction.id}

    except Exception as e:
        db.rollback()
        raise HTTPException(500, detail=f"Ошибка при создании транзакции: {str(e)}")


@router.get("/transaction-types/", response_model=list[TransactionTypeSchema])
def get_transaction_types(db: Session = Depends(get_db)):
    """
    Для фронта, формирование выпадающего списка типа транзакции
    :param db:
    :return:
    """
    return db.query(models.TransType).all()


@router.get("/category-types/", response_model=list[CategorySchema])
def get_category(db: Session = Depends(get_db)):
    """Для фронта, формирование выпадающего списка категорий пользователя"""
    return db.query(models.Category).all()


@router.get("/transaction-status/", response_model=list[TransactionStatusSchema])
def get_trans_status(db: Session = Depends(get_db)):
    return db.query(models.TransStatus).all()


@router.get("/person-type/", response_model=list[PersonTypeSchema])
def get_trans_status(db: Session = Depends(get_db)):
    return db.query(models.PersonType).all()
