from fastapi import HTTPException, status
from app.schema.movie_schema import MovieCreateSchema, CastCreateSchema
from app.models.movie_model import Movie, Cast
from app.database import session

""" START MOVIE OPERATIONS """


def get_all_movies(db: session):
    return db.query(Movie).all()


def add_movie(movie: MovieCreateSchema, db: session):
    try:
        with session.begin():
            new_movie = Movie(
                title=movie.title,
                length=movie.length,
                description=movie.description,
                cover_image_url=movie.cover_image_url
            )

            db.add(new_movie)
            db.commit()
            db.refresh(new_movie)

            return new_movie
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def get_movie(movie_id, db: session):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Movie with ID: {movie_id} not found!')
    return movie


def update_movie(movie_id: int, movie: MovieCreateSchema, db: session):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if db_movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Movie with ID: {movie_id} not found!')
    db_movie.description = movie.description
    db_movie.cover_image_url = movie.cover_image_url
    db_movie.length = movie.length
    db_movie.title = movie.title

    db.commit()
    db.refresh(db_movie)

    return db_movie


def delete_movie(movie_id: int, db: session):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if db_movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Movie with ID: {movie_id} not found!')

    db.delete(db_movie)
    db.commit()

    """ END MOVIE OPERATIONS"""

    """ START CAST OPERATIONS"""


def get_movie_casts(movie_id: int, db: session):
    return db.query(Cast).filter(Cast.movie_id == movie_id).all()


def add_cast(cast: CastCreateSchema, db: session):
    try:
        with session.begin():
            new_cast = Cast(full_anme=cast.full_anme)

            db.add(new_cast)
            db.commit()
            db.refresh(new_cast)

            return new_cast

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def update_cast(cast_id: int, movie: CastCreateSchema, db: session):
    db_cast = db.query(Cast).filter(Cast.id == cast_id).first()

    if db_cast is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Cast with ID: {db_cast} not found!')
    db_cast.full_name = movie.full_name

    db.commit()
    db.refresh(db_cast)

    return db_cast


def delete_cast(cast_id: int, db: session):
    db_cast = db.query(Cast).filter(Cast.id == cast_id).first()

    if db_cast is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Cast with ID: {cast_id} not found!')

    db.delete(db_cast)
    db.commit()

    """ END CAST OPERATIONS"""
