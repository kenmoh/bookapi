from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schema.book_schema import BookCreateSchema, BookResponseSchema
from app.services import book_services


book_router = APIRouter(tags=['Books'], prefix='/books')


@book_router.get('', status_code=status.HTTP_200_OK)
def get_books(db: Session = Depends(get_db)) -> list[BookResponseSchema]:
    return book_services.get_all_books(db=db)


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
    return book_services.delete_book(book_id, db)
