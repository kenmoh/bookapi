from datetime import datetime
from pydantic import BaseModel, Field


class ReviewCreateSchema(BaseModel):
    author: str
    comment: str
    rating: int | None = Field(gt=0, le=5)


class ReviewResponseSchema(ReviewCreateSchema):
    id: int
    movie_id: int
    created_at: datetime


class AverageMovieRating(BaseModel):
    average_rating: float
