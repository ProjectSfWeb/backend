from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import get_db
import models
from models import User
from utils.jwt import get_current_user


router = APIRouter(tags=["Filters"])


@router.get("/transactions/filter/")
def filter_transactions(
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
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Роут для кнопки 'Apply Filters'
    Возвращает данные для дашбордов, и транзакции, соответствующие фильтрам

    Принимает query парасметры для фильтрации подходящих транзакций
    :return: Возвращает данные для дашбордов, и транзакции, соответствующие фильтрам
    """
    query = db.query(models.Transaction).filter(models.Transaction.user_id == current_user.id)

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
    # --- DASHBOARDS ---

    base_query = query.with_entities(models.Transaction.timestamp, models.Transaction.amount,
                                     models.Transaction.transTypeID, models.Transaction.status_id,
                                     models.Transaction.sender_bank, models.Transaction.receiver_bank,
                                     models.Transaction.category_id)

    #  1. Динамика по месяцам (группировка по месяцу)
    by_month = (
        db.query(
            func.date_trunc('month', models.Transaction.timestamp).label("period"),
            func.count().label("count")
        )
        .filter(models.Transaction.user_id == current_user.id)
        .group_by("period")
        .order_by("period")
        .all()
    )
    by_month = [{"period": p[0].strftime("%Y-%m"), "count": p[1]} for p in by_month]

    #  2. Динамика по типу транзакции
    by_trans_type = (
        db.query(
            models.Transaction.transTypeID,
            func.count().label("count")
        )
        .filter(models.Transaction.user_id == current_user.id)
        .group_by(models.Transaction.transTypeID)
        .all()
    )
    by_trans_type = [{"trans_type": t[0], "count": t[1]} for t in by_trans_type]

    #  3. Сравнение поступивших и потраченных
    credit_vs_debit = (
        db.query(
            models.Transaction.transTypeID,
            func.sum(models.Transaction.amount)
        )
        .filter(models.Transaction.user_id == current_user.id)
        .group_by(models.Transaction.transTypeID)
        .all()
    )
    credit_vs_debit = {f"type_{r[0]}": r[1] for r in credit_vs_debit}

    #  4. Проведенные vs отмененные (по статусу)
    by_status = (
        db.query(
            models.Transaction.status_id,
            func.count()
        )
        .filter(models.Transaction.user_id == current_user.id)
        .group_by(models.Transaction.status_id)
        .all()
    )
    by_status = {f"status_{r[0]}": r[1] for r in by_status}

    #  5. Статистика по банкам отправителя и получателя
    by_banks = {
        "sender": dict(db.query(models.Transaction.sender_bank, func.count())
                       .filter(models.Transaction.user_id == current_user.id)
                       .group_by(models.Transaction.sender_bank).all()),
        "receiver": dict(db.query(models.Transaction.receiver_bank, func.count())
                         .filter(models.Transaction.user_id == current_user.id)
                         .group_by(models.Transaction.receiver_bank).all()),
    }

    #  6. По категориям расходов/поступлений
    by_categories = dict(db.query(models.Transaction.category_id, func.count())
                         .filter(models.Transaction.user_id == current_user.id)
                         .group_by(models.Transaction.category_id)
                         .all())

    return {
        "transactions": transactions,
        "dashboards": {
            "by_month": by_month,
            "by_trans_type": by_trans_type,
            "credit_vs_debit": credit_vs_debit,
            "by_status": by_status,
            "by_banks": by_banks,
            "by_categories": by_categories,
        }
    }