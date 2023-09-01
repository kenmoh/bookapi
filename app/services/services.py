from fastapi import HTTPException, status
from app.schema.movie_schema import MovieCreateSchema
from app.models.movie_model import Movie
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
                cover_image_url=movie.cover_image_url,
                casts=movie.casts,
                thriller=movie.thriller,
                genre=movie.genre
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
    db.casts = movie.casts
    db.thriller = movie.thriller
    db.genre = movie.genre

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
