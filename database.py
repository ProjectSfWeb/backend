import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Замените на свои данные
DB_USER = os.environ.get("DATABASE_USER")
DB_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DB_HOST = os.environ.get("DATABASE_HOST")
DB_PORT = os.environ.get("DATABASE_PORT")
DB_NAME = os.environ.get("DATABASE_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)