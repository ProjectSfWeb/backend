from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models


router = APIRouter(tags=["Filters"])


@router.get("/transactions/filter/")
def filter_transactions(
        user_id: int,
        start_date: str = None,
        end_date: str = None,
        exact_date: str = None,
        sender_bank: str = None,
        receiver_bank: str = None,
        status: int = None,
        inn: str = None,
        operation_min: str = None,
        operation_max: str = None,
        trans_type: int = None,
        category: int = None,
        db: Session = Depends(get_db)
):
    """Роут для кнопки 'Apply Filters'"""
    query = db.query(models.Transaction).filter(models.Transaction.user_id == user_id)

    if exact_date:
        query = query.filter(models.Transaction.timestamp == exact_date)
    if start_date:
        query = query.filter(models.Transaction.timestamp >= start_date)
    if end_date:
        query = query.filter(models.Transaction.timestamp <= end_date)
    if sender_bank:
        query = query.filter(models.Transaction.sender_bank == sender_bank)
    if receiver_bank:
        query = query.filter(models.Transaction.receiver_bank == receiver_bank)
    if status:
        query = query.filter(models.Transaction.status_id == status)
    if inn:
        query = query.filter(models.Transaction.rec_inn == inn)
    if operation_max:
        query = query.filter(models.Transaction.amount <= operation_max)
    if operation_min:
        query = query.filter(models.Transaction.amount >= operation_min)
    if trans_type:
        query = query.filter(models.Transaction.transTypeID == trans_type)
    if category:
        query = query.filter(models.Transaction.category_id == category)
    transactions = query.all()
    return {"transactions": transactions}