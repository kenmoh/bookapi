from pydantic import BaseModel, Field


""" START MOVIE SCHEMA """


class MovieCreateSchema(BaseModel):
    title: str = Field(min_length=1, max_length=50, description='Movie title')
    length: float = Field(description='Movie duration')
    description: str = Field(max_length=225, description='Summary of the book')
    casts: str = Field(description="List of casts separated by comma")
    genre: str
    thriller: str


class MovieResponseSchema(MovieCreateSchema):
    id: int
    cover_image_url: str


""" END MOVIE SCHEMA"""

""" START REVIEW SCHEMA """


class ReviewResponseSchema(BaseModel):
    movie_id: int
    author: str
    comment: str
    rating: int | None


class ReviewCreateSchema(BaseModel):
    author: str
    comment: str
    rating: int = Field(gt=0, le=5)


class AverageMovieReview(BaseModel):
    average_rating: float


""" END REVIEW SCHEMA"""
