from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.books import BookCreate
from app.db.models import Book


async def add_book(db: AsyncSession, data: BookCreate) -> Book:
    """Добавляет книгу в дневник пользователя."""
    book = Book(
        title=data.title,
        author=data.author,
        rating=data.rating,
        review=data.review,
    )
    db.add(book)
    await db.commit()
    await db.refresh(book) # получаем id
    return book

async def get_all_book(db: AsyncSession) -> list[Book]:
    """Возвращает все книги из дневника."""
    result = await db.execute(select(Book).order_by(Book.created_at.desc()))
    return list(result.scalars().all())