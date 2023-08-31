from pydantic import BaseModel, Field


""" START MOVIE SCHEMA """


class MovieCreateSchema(BaseModel):
    title: str = Field(min_length=1, max_length=50, title='Movie title')
    length: float = Field(title='Movie duration')
    description: str = Field(max_length=225, title='Summary of the book')
    cover_image_url: str = Field(title='Movie cover image')
    casts: str = Field(title="List of casts separated by comma")


class MovieResponseSchema(MovieCreateSchema):
    id: int


""" END MOVIE SCHEMA"""

""" START REVIEW SCHEMA """


class ReviewResponseSchema(BaseModel):
    book_id: int
    review_body: str
    review_by: str
    rating: int | None


class ReviewCreateSchema(BaseModel):
    review_by: str
    review_body: str
    rating: int = Field(gt=0, le=5)


""" END REVIEW SCHEMA"""
