from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from database import get_db
import models

router = APIRouter(tags=["Balance"])

@router.get("/balance/")
def calculate_balance(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Расчет баланса доходов и расходов"""
    # Запрос для суммы доходов (transTypeID=1)
    income = db.query(func.sum(models.Transaction.amount)).filter(
        and_(
            models.Transaction.user_id == user_id,
            models.Transaction.transTypeID == 0  # income
        )
    ).scalar() or 0

    # Запрос для суммы расходов (transTypeID=2)
    expense = db.query(func.sum(models.Transaction.amount)).filter(
        and_(
            models.Transaction.user_id == user_id,
            models.Transaction.transTypeID == 1  # expense
        )
    ).scalar() or 0

    return {
        "balance": income - expense,
        "total_income": income,
        "total_expense": expense
    }