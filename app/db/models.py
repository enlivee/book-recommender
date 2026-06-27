from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime


class Base(DeclarativeBase):
    ...

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False)
    author = Column(String(300), nullable=False)
    rating = Column(Float, nullable=True)  # Оценка пользователя (1-10)
    review = Column(Text, nullable=True)  # Отзыв
    created_at = Column(DateTime, default=datetime.utcnow)