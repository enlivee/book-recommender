from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    """То, что присылает пользователь при добавлении книги."""
    title: str = Field(..., min_length=1, max_length=500)
    author: str = Field(..., min_length=1, max_length=500)
    rating: float | None = Field(None, ge=1, le=10)  # от 1 до 10
    review: str | None = Field(None, max_length=5000)

class BookResponse(BaseModel):
    """То, что мы возвращаем пользователю."""
    id: int
    title: str
    author: str
    rating: float | None
    review: str | None

    model_config = {"from_attributes": True}  # Чтобы работало с SQLAlchemy