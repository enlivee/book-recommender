from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import Book
from app.schemas.books import BookCreate
from app.tasks.tasks import generate_embedding_for_book, recalculate_recommendations

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
    generate_embedding_for_book.delay(book.id)
    return book

async def get_all_book(db: AsyncSession) -> list[Book]:
    """Возвращает все книги из дневника."""
    result = await db.execute(select(Book).order_by(Book.created_at.desc()))
    return list(result.scalars().all())