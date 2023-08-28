from pydantic import BaseModel, Field


class BookCreateSchema(BaseModel):
    author: str = Field(min_length=1, max_length=75, title='Name of the author')
    title: str = Field(min_length=1, max_length=50, title='Book title')
    description: str | None = Field(max_length=100, title='Summary of the book')
    isbn: str


class BookResponseSchema(BookCreateSchema):
    id: int
    rating: int | None = Field(gt=0, le=5)


class ReviewResponseSchema(BaseModel):
    book_id: int
    review_body: str
    review_by: str
    rating: int | None


class ReviewCreateSchema(BaseModel):
    review_by: str
    review_body: str
    rating: int = Field(gt=0, le=5)
