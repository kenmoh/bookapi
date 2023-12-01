from fastapi import HTTPException, status

from app.models.movie_model import Review
from app.database import session
from app.schema.review_schema import ReviewCreateSchema


def get_all_reviews(db: session):
    try:
        return db.query(Review).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


def add_new_review(
    movie_id: int, ip_address: str, review: ReviewCreateSchema, db: session
):
    existing_review = db.query(Review).filter(Review.movie_id == movie_id, Review.ip_address == ip_address).first()
    ratings = db.query(Review).filter(Review.movie_id == movie_id).all()

    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="You already reviewed this movie."
        )
    try:
        with session.begin():
            new_review = Review(
                movie_id=movie_id,
                author=review.author,
                comment=review.comment,
                rating=review.rating,
                ip_address=ip_address,

            )
            db.add(new_review)
            db.commit()
            db.refresh(new_review)

            return new_review
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="You already reviewed this movie."
        )


def get_all_reviews_by_movie(movie_id, db: session):
    try:
        return db.query(Review).filter(Review.movie_id == movie_id).all()
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


def get_average_rating_by_movie(movie_id, db: session):
    try:
        ratings = db.query(Review).filter(Review.movie_id == movie_id).all()
        if len(ratings) > 0:
            return {
                "average_rating": sum([rating.rating for rating in ratings])
                / len(ratings)
            }
        return 0
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


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
