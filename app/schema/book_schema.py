from uuid import UUID
from pydantic import BaseModel, Field


class BookSchema(BaseModel):
    id: UUID
    author: str = Field(min_length=1, max_length=75, title='Name of the author')
    title: str = Field(min_length=1, max_length=50, title='Book title')
    description: str | None = Field(max_length=100, title='Summary of the book')
    isbn: str
    rating: int = Field(ge=1, le=5)

