from fastapi import APIRouter, Depends, status, HTTPException
import requests
from sqlalchemy.orm import Session

from app.database import get_db
from app.schema.book_schema import BookCreateSchema, BookResponseSchema, ReviewResponseSchema, ReviewCreateSchema
from app.services import book_services


book_router = APIRouter(tags=['Books'], prefix='/api/books')
REVIEW_URL = 'https://reviewapi.onrender.com/api/reviews'


@book_router.get('', status_code=status.HTTP_200_OK)
def get_books(db: Session = Depends(get_db)) -> list[BookResponseSchema]:
    return book_services.get_all_books(db)


@book_router.post('', status_code=status.HTTP_201_CREATED)
def add_new_book(book: BookCreateSchema, db: Session = Depends(get_db)) -> BookResponseSchema:
    return book_services.add_book(book, db)


@book_router.put('/{book_id}',  status_code=status.HTTP_202_ACCEPTED)
def update_book(book_id, book: BookCreateSchema, db: Session = Depends(get_db)) -> BookResponseSchema:
    return book_services.update_book(book_id, book, db)


@book_router.get('/{book_id}', status_code=status.HTTP_200_OK)
def get_book(book_id, db: Session = Depends(get_db)) -> BookResponseSchema:
    return book_services.get_book(book_id, db)


@book_router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    requests.delete(f'{REVIEW_URL}/delete-reviews/{book_id}')
    return book_services.delete_book(book_id, db)


@book_router.get('/reviews/{book_id}', status_code=status.HTTP_200_OK)
def get_book_reviews(book_id: int) -> list[ReviewResponseSchema]:
    response = requests.get(f'{REVIEW_URL}/{book_id}')
    data: list = response.json()
    return data


@book_router.post('/reviews/{book_id}', status_code=status.HTTP_201_CREATED)
def add_review(book_id: int, review: ReviewCreateSchema, db: Session = Depends(get_db)) -> ReviewResponseSchema:
    book = book_services.get_book(book_id, db)
    data = {
       "review_body": review.review_body, "review_by": review.review_by, 'rating': review.rating
    }
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Book with ID: {book_id} not found!')
    response = requests.post(f'{REVIEW_URL}/{book_id}', json=data)
    data = response.json()
    return data


@book_router.get('/average-rating/{book_id}', status_code=status.HTTP_200_OK)
def get_avg_book_rating(book_id: int) -> float:
    response = requests.get(f'{REVIEW_URL}/average-rating/{book_id}')
    avg_rating: float = response.json()
    return avg_rating
