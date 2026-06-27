from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.books import BookCreate, BookResponse
from app.services import book_service

router = APIRouter(prefix="/api/books", tags=["books"])

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def add_book(
        data: BookCreate,
        db: AsyncSession = Depends(get_db),
):
    book = await book_service.add_book(db, data)
    return book

@router.get("/", response_model=list[BookResponse], status_code=status.HTTP_200_OK)
async def get_books(db: AsyncSession = Depends(get_db)):
    return await book_service.get_all_book(db)

# @router.delete("/{book_id}", response_model=BookDelete, status_code=status.HTTP_204_NO_CONTENT)
# async def delete_book(
#         book_id: int,
#         db: AsyncSession = Depends(get_db),
# ):
#     books = await book_service.get_all_book(db)
#     books = [book for book in books if book.id != book_id]
#     return books