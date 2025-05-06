from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from database import get_db
from utils.jwt import get_current_user
import models
from models import User
from io import BytesIO
from fastapi.responses import StreamingResponse
import pandas as pd

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


@router.get("/excel", response_class=StreamingResponse)
async def get_transactions_excel(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Выгружает транзакции текущего пользователя в Excel-файл.
    Требует аутентификации.
    """

    transactions = db.query(models.Transaction).filter(models.Transaction.user_id == current_user.id).all()

    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found for this user")

    transaction_data = []
    for transaction in transactions:
        transaction_data.append({
            "ID": transaction.id,
            "Дата и время": transaction.timestamp,
            "Сумма": transaction.amount,
            "Тип транзакции": transaction.trans_type.name if transaction.trans_type else None,
            "Статус": transaction.trans_status.name if transaction.trans_status else None,
            "Категория": transaction.category.name if transaction.category else None,
            "Тип лица": transaction.person_type.name if transaction.person_type else None,
            "Комментарий": transaction.comment,
            "Банк отправителя": transaction.sender_bank,
            "Банк получателя": transaction.receiver_bank,
            "Счет": transaction.account,
            "ИНН получателя": transaction.rec_inn,
            "Счет получателя": transaction.rec_acc,
            "Телефон получателя": transaction.rec_phone,
        })

    df = pd.DataFrame(transaction_data)

    excel_file = BytesIO()
    df.to_excel(excel_file, index=False, sheet_name="Transactions")

    excel_file.seek(0)

    headers = {
        'Content-Disposition': 'attachment; filename="transactions.xlsx"'
    }

    return StreamingResponse(excel_file, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)