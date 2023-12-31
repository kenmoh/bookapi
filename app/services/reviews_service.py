from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy import desc
from app.models.movie_model import Review
from app.database import session
from app.schema.review_schema import ReviewCreateSchema


def get_all_reviews(db: session):
    try:
        return db.query(Review).order_by(desc(Review.created_at)).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


def add_new_review(
    movie_id: int, ip_address: str, review: ReviewCreateSchema, db: session
):
    existing_review = (
        db.query(Review)
        .filter(Review.movie_id == movie_id, Review.ip_address == ip_address)
        .first()
    )

    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already reviewed this movie!",
        )

    new_review = Review(
        movie_id=movie_id,
        author=review.author,
        comment=review.comment,
        rating=review.rating,
        ip_address=ip_address,
        created_at=datetime.now(),
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return new_review


def get_all_reviews_by_movie(movie_id, db: session):
    try:
        return db.query(Review).filter(Review.movie_id == movie_id).order_by(desc(Review.created_at)).all()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


def delete_review(review_id: int, db: session):
    db_movie_review = db.query(Review).filter(Review.id == review_id).first()

    if not db_movie_review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with ID: {review_id} not found!",
        )

    db.delete(db_movie_review)
    db.commit()


def delete_movie_reviews(movie_id: int, db: session):
    db_movie_reviews = db.query(Review).filter(Review.movie_id == movie_id).all()

    if not db_movie_reviews:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID: {movie_id} not found!",
        )
    for db_movie_review in db_movie_reviews:
        db.delete(db_movie_review)
        db.commit()
