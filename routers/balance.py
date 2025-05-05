from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from database import get_db
import models
from models import User
from utils.jwt import get_current_user
router = APIRouter(tags=["Balance"])

@router.get("/balance/")
def calculate_balance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Расчет баланса доходов и расходов"""
    # Запрос для суммы доходов (transTypeID=0)
    income = db.query(func.sum(models.Transaction.amount)).filter(
        and_(
            models.Transaction.user_id == current_user.id,
            models.Transaction.transTypeID == 0  # income
        )
    ).scalar() or 0

    # Запрос для суммы расходов (transTypeID=1)
    expense = db.query(func.sum(models.Transaction.amount)).filter(
        and_(
            models.Transaction.user_id == current_user.id,
            models.Transaction.transTypeID == 1  # expense
        )
    ).scalar() or 0

    return {
        "balance": income - expense,
        "total_income": income,
        "total_expense": expense
    }