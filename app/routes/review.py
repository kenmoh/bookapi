from fastapi import APIRouter, status,  Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schema.review_schema import ReviewResponseSchema, ReviewCreateSchema, AverageMovieRating
from app.services import reviews


review_router = APIRouter(prefix='/api/reviews', tags=['Review'])


@review_router.get('', status_code=status.HTTP_200_OK)
def get_reviews(db: Session = Depends(get_db)) -> list[ReviewResponseSchema]:
    return reviews.get_all_reviews(db)


@review_router.post('/{movie_id}', status_code=status.HTTP_201_CREATED)
def add_review(movie_id, review: ReviewCreateSchema, db: Session = Depends(get_db)) -> ReviewResponseSchema:
    return reviews.add_new_review(movie_id, review, db)


@review_router.get('/{movie_id}', status_code=status.HTTP_200_OK)
def get_movie_reviews(movie_id: int, db: Session = Depends(get_db)) -> list[ReviewResponseSchema]:
    return reviews.get_all_reviews_by_movie(movie_id, db)


@review_router.get('/average-rating/{movie_id}', status_code=status.HTTP_200_OK)
def get_movie_avg_rating(movie_id: int, db: Session = Depends(get_db)) -> AverageMovieRating:
    return reviews.get_average_rating_by_movie(movie_id, db)


@review_router.delete('/delete-reviews/{movie_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_movie_reviews(movie_id: int, db: Session = Depends(get_db)):
    return reviews.delete_movie_reviews(movie_id, db)


@review_router.delete('/delete-review/{review_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_movie_reviews(review_id: int, db: Session = Depends(get_db)):
    return reviews.delete_review(review_id, db)
