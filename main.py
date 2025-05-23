import uvicorn
from fastapi import FastAPI
from database import engine
import models

from routers import balance, filters, transactions, auth, transaction_excel, view

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(balance.router)
app.include_router(filters.router)
app.include_router(transactions.router)
app.include_router(auth.router)
app.include_router(transaction_excel.router)
app.include_router(view.router)

@app.get("/")
def read_root():
    return {"message": "FastAPI is running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)