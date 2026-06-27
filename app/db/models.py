from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
from pgvector.sqlalchemy import Vector


class Base(DeclarativeBase):
    ...

class Book(Base):
    """Дневник пользователя: прочитанные книги."""
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False)
    author = Column(String(300), nullable=False)
    rating = Column(Float, nullable=True)
    review = Column(Text, nullable=True)
    embedding = Column(Vector(768), nullable=True)  # эмбеддинг описания
    created_at = Column(DateTime, default=datetime.now)

class CatalogBook(Base):
    """Каталог книг, из которого мы рекомендуем."""
    __tablename__ = "catalog"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False)
    author = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    embedding = Column(Vector(768), nullable=True)

class Recommendation(Base):
    """Персональные рекомендации для пользователя."""
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    catalog_book_id = Column(Integer, ForeignKey("catalog.id"), nullable=False)
    score = Column(Float, nullable=False)  # косинусное расстояние (чем меньше, тем ближе)
    created_at = Column(DateTime, default=datetime.now)