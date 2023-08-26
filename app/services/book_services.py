from fastapi import HTTPException, status
from app.schema.book_schema import BookCreateSchema
from app.models.book_model import Book
from app.database import session


def get_all_books(db: session):
    return db.query(Book).all()


def add_book(book: BookCreateSchema, db: session):
    try:
        with session.begin():
            new_book = Book(
                author=book.author,
                title=book.title,
                description=book.description,
                isbn=book.isbn,
            )

            db.add(new_book)
            db.commit()
            db.refresh(new_book)

            return new_book
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def get_book(book_id, db: session):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Book with ID: {book_id} not found!')
    return book


def update_book(book_id: int, book: BookCreateSchema, db: session):
    db_book = db.query(Book).filter(Book.id == book_id).first()

    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Book with ID: {book_id} not found!')
    db_book.author = book.author
    db_book.title = book.title
    db_book.description = book.description
    db_book.isbn = book.isbn

    db.commit()
    db.refresh(db_book)

    return db_book


def delete_book(book_id: int, db: session):
    db_book = db.query(Book).filter(Book.id == book_id).first()

    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Book with ID: {book_id} not found!')

    db.delete(db_book)
    db.commit()

