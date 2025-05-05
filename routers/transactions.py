from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from datetime import datetime, timedelta
from models import User
from utils.jwt import get_current_user
from schemas.service_schemes import (TransactionCreate, TransactionTypeSchema, CategorySchema,
                                     TransactionStatusSchema, PersonTypeSchema, TransactionUpdate)

router = APIRouter(tags=["Transactions"])


@router.post("/transactions/", status_code=201)
def create_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Роут для добавления транзакции.
    Валидирует инн, номер телефона. Также принимает категорию транзакции.
    В случае, если пользователь ранее не вносил подобную категорию, данная категория записывается в базу данных.
    Привязывается к конкретному пользователю
    """
    try:
        # Проверка, есть ли такая категория уже
        category = db.query(models.Category).filter_by(name=data.category_name,
                                                       user_id=current_user.id).first()
        if not category:
            # Если нет — создаём новую
            category = models.Category(name=data.category_name, user_id=current_user.id)
            db.add(category)
            db.commit()
            db.refresh(category)

        # Создаём объект транзакции
        transaction = models.Transaction(
            user_id=current_user.id,
            transTypeID=data.transTypeID,
            category_id=category.id,
            amount=data.amount,
            comment=data.comment,
            timestamp=datetime.utcnow(),
            status_id=0,  # по умолчанию статус
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


@router.put("/transactions/{transaction_id}")
def edit_transaction(
    transaction_id: int,
    data: TransactionUpdate,  # это твоя схема для редактирования
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Обновление транзакции
    :param transaction_id:
    :param data:
    :param db:
    :param current_user:
    :return:
    """
    transaction = db.query(models.Transaction).filter_by(id=transaction_id, user_id=current_user.id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Транзакция не найдена")

    if transaction.status_id != 0:
        raise HTTPException(status_code=403, detail="Редактирование запрещено — статус не 'новая'")

    # time_passed = datetime.utcnow() - transaction.timestamp
    # if time_passed > timedelta(minutes=1):
    #     raise HTTPException(status_code=403, detail="Редактирование запрещено — статус не 'новая'")

    category = db.query(models.Category).filter_by(name=data.category_name,
                                                   user_id=current_user.id).first()
    if not category:
        # Если нет — создаём новую
        category = models.Category(name=data.category_name, user_id=current_user.id)
        db.add(category)
        db.commit()
        db.refresh(category)

    # Теперь обновляем нужные поля
    transaction.person_typeID = data.person_typeID
    transaction.timestamp = data.timestamp
    transaction.comment = data.comment
    transaction.amount = data.amount
    transaction.status_id = data.status_id
    transaction.sender_bank = data.sender_bank
    transaction.receiver_bank = data.receiver_bank
    transaction.rec_inn = data.rec_inn
    transaction.category_id = category.id
    transaction.rec_phone = data.rec_phone

    db.commit()
    db.refresh(transaction)

    return {"status": "updated", "transaction_id": transaction.id}


DELETED_STATUS_ID = 5

# Запрещенные для удаления статусы
FORBIDDEN_TO_DELETE = {1, 2, 3, 4, 6}

@router.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    """
    Удаление транзакции
    :param transaction_id:
    :param db:
    :param current_user:
    :return:
    """
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.user_id == current_user.id
    ).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Транзакция не найдена")

    if transaction.status_id in FORBIDDEN_TO_DELETE:
        raise HTTPException(status_code=403, detail="Удаление запрещено для текущего статуса транзакции")

    transaction.status_id = DELETED_STATUS_ID
    db.commit()
    db.refresh(transaction)

    return {"status": "success", "message": "Транзакция помечена как удалённая"}

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
