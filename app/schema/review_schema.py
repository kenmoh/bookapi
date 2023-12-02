from pydantic import BaseModel, Field


class ReviewCreateSchema(BaseModel):
    author: str
    comment: str
    rating: int | None = Field(gt=0, le=5)


class ReviewResponseSchema(ReviewCreateSchema):
    id: int
    movie_id: int


class AverageMovieRating(BaseModel):
    average_rating: float
