from pydantic import BaseModel, Field

""" START CAST SCHEMA"""


class CastCreateSchema(BaseModel):
    full_name: str


class CastResponseSchema(CastCreateSchema):
    id: int
    movie_id: int


""" END CAST SCHEMA """

""" START MOVIE SCHEMA """


class MovieCreateSchema(BaseModel):
    title: str = Field(min_length=1, max_length=50, title='Movie title')
    length: str = Field(min_length=1, max_length=75, title='Movie duration')
    description: str = Field(max_length=225, title='Summary of the book')
    cover_image_url: str = Field(title='Movie cover image')


class MovieResponseSchema(MovieCreateSchema):
    id: int
    casts: list[CastResponseSchema] | None


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
