import uvicorn
from fastapi import FastAPI
from database import engine
import models

app = FastAPI()

# Создаём таблицы
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "FastAPI is running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)