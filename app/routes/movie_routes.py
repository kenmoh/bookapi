from fastapi import APIRouter, Depends, status, HTTPException
import requests
from sqlalchemy.orm import Session

from app.database import get_db
from app.schema.movie_schema import MovieCreateSchema, MovieResponseSchema, ReviewResponseSchema, ReviewCreateSchema
from app.services import services


book_router = APIRouter(tags=['Movies'], prefix='/api/movies')
REVIEW_URL = 'https://reviewapi.onrender.com/api/reviews'


@book_router.get('', status_code=status.HTTP_200_OK)
def get_movies(db: Session = Depends(get_db)) -> list[MovieResponseSchema]:
    return services.get_all_movies(db)


@book_router.post('', status_code=status.HTTP_201_CREATED)
def add_new_movie(movie: MovieCreateSchema, db: Session = Depends(get_db)) -> MovieResponseSchema:
    return services.add_movie(movie, db)


@book_router.put('/{movie_id}',  status_code=status.HTTP_202_ACCEPTED)
def update_movie(movie_id, movie: MovieCreateSchema, db: Session = Depends(get_db)) -> MovieResponseSchema:
    return services.update_movie(movie_id, movie, db)


@book_router.get('/{movie_id}', status_code=status.HTTP_200_OK)
def get_movie(movie_id, db: Session = Depends(get_db)) -> MovieResponseSchema:
    return services.get_movie(movie_id, db)


@book_router.delete('/{movie_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    requests.delete(f'{REVIEW_URL}/delete-reviews/{movie_id}')
    return services.delete_movie(movie_id, db)


@book_router.get('/reviews/{movie_id}', status_code=status.HTTP_200_OK)
def get_movie_reviews(movie_id: int) -> list[ReviewResponseSchema]:
    response = requests.get(f'{REVIEW_URL}/{movie_id}')
    data: list = response.json()
    return data


@book_router.post('/reviews/{movie_id}', status_code=status.HTTP_201_CREATED)
def add_review(movie_id: int, review: ReviewCreateSchema, db: Session = Depends(get_db)) -> ReviewResponseSchema:
    movie = services.get_movie(movie_id, db)
    data = {
       "review_body": review.review_body, "review_by": review.review_by, 'rating': review.rating
    }
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Movie with ID: {movie_id} not found!')
    response = requests.post(f'{REVIEW_URL}/{movie_id}', json=data)
    data = response.json()
    return data


@book_router.get('/average-rating/{book_id}', status_code=status.HTTP_200_OK)
def get_avg_movie_rating(movie_id: int) -> float:
    response = requests.get(f'{REVIEW_URL}/average-rating/{movie_id}')
    avg_rating: float = response.json()
    return avg_rating
