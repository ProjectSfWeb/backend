from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, DateTime
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    password_hash = Column(String)
    categories = relationship("Category", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category")


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    transTypeID = Column(BigInteger, ForeignKey("trans_type.id"))
    status_id = Column(BigInteger, ForeignKey("trans_status.id"))
    category_id = Column(BigInteger, ForeignKey("category.id"))
    person_typeID = Column(Integer, ForeignKey("person_type.id"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)  # Дата и время транзакции
    amount = Column(BigInteger)
    comment = Column(String)
    sender_bank = Column(String)
    receiver_bank = Column(String)
    account = Column(String)
    rec_inn = Column(String)
    rec_acc = Column(String)
    rec_phone = Column(String)

    user = relationship("User", back_populates="transactions")
    trans_type = relationship("TransType", back_populates="transactions")
    trans_status = relationship("TransStatus", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
    person_type = relationship("PersonType", back_populates="transactions")


class TransType(Base):
    __tablename__ = "trans_type"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String)
    transactions = relationship("Transaction", back_populates="trans_type")


class TransStatus(Base):
    __tablename__ = "trans_status"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String)
    transactions = relationship("Transaction", back_populates="trans_status")

class PersonType(Base):
    __tablename__ = "person_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    transactions = relationship("Transaction", back_populates="person_type")