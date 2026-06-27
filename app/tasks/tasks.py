from app.tasks.celery_app import app
from app.db.session import async_session
from app.db.models import Book, CatalogBook, Recommendation
from app.services.embedding_service import get_embedding
from sqlalchemy import select, delete, func
import asyncio


@app.task
def generate_embedding_for_book(book_id: int):
    """Генерирует эмбеддинг для книги из дневника пользователя."""
    async def _run():
        async with async_session() as db:
            book = await db.get(Book, book_id)
            if not book or book.embedding is not None:
                return  # уже есть эмбеддинг или книга не найдена

            text = f"{book.title}. {book.author}."
            if book.review:
                text += f" Отзыв: {book.review}"

            embedding = await get_embedding(text)
            book.embedding = embedding
            await db.commit()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_run())


@app.task
def generate_embeddings_for_catalog():
    """Генерирует эмбеддинги для всех книг в каталоге, у которых их нет."""
    async def _run():
        async with async_session() as db:
            result = await db.execute(
                select(CatalogBook).where(CatalogBook.embedding.is_(None))
            )
            books = result.scalars().all()

            for book in books:
                text = f"{book.title}. {book.author}."
                if book.description:
                    text += f" {book.description}"
                book.embedding = await get_embedding(text)

            await db.commit()
            print(f"Эмбеддинги сгенерированы для {len(books)} книг каталога")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_run())


@app.task
def recalculate_recommendations():
    """Пересчитывает персональные рекомендации на основе всех книг в дневнике."""
    async def _run():
        async with async_session() as db:
            # Берем эмбеддинги всех прочитанных книг
            result = await db.execute(
                select(Book.embedding).where(Book.embedding.isnot(None))
            )
            user_embeddings = result.scalars().all()

            if not user_embeddings:
                print("Нет книг с эмбеддингами — нечего рекомендовать")
                return

            # Средний вектор вкуса
            taste_vector = [
                sum(dim) / len(user_embeddings)
                for dim in zip(*user_embeddings)
            ]

            # Ищем 10 ближайших книг из каталога
            nearest = await db.execute(
                select(CatalogBook)
                .where(CatalogBook.embedding.isnot(None))
                .order_by(CatalogBook.embedding.cosine_distance(taste_vector))
                .limit(10)
            )
            nearest_books = nearest.scalars().all()

            # Очищаем старые и сохраняем новые рекомендации
            await db.execute(delete(Recommendation))
            for i, book in enumerate(nearest_books):
                db.add(Recommendation(
                    catalog_book_id=book.id,
                    score=float(i),  # порядковый номер как скор
                ))
            await db.commit()
            print(f"Рекомендации обновлены: {len(nearest_books)} книг")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_run())