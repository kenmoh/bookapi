from fastapi import HTTPException, status
from app.models.movie_model import Movie
from app.database import session
from app.forms import AddMovieForm
from app.utils import delete_image
from app.services.reviews_service import get_all_reviews_by_movie

""" START MOVIE OPERATIONS """


def get_all_movies(db: session):
    """
    This function
    gets all movies from the database
    :param db:
    :return: All movies in the database
    """
    movies = db.query(Movie).all()
    for movie in movies:
        reviews = get_all_reviews_by_movie(movie.id, db)

        if reviews:
            average_rating = sum(review.rating for review in reviews) / len(reviews)
            movie.average_rating = average_rating
        else:
            movie.average_rating = 0.0

    return movies


def add_movie(movie: AddMovieForm, db: session):
    """
    Add new movie to the database service
    """
    try:
        with session.begin():
            new_movie = Movie(
                title=movie.title,
                length=movie.length,
                description=movie.descr,
                cover_image_url=movie.image,
                casts=movie.casts,
                thriller=movie.thriller,
                genre=movie.genre,
            )

            db.add(new_movie)
            db.commit()
            db.refresh(new_movie)

            return new_movie
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


def get_movie(movie_id, db: session):
    """
    This function retrieves a single movie from the database
    :param movie_id:
    :param db:
    :return: Movie object
    """
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with ID: {movie_id} not found!",
        )
    if movie.reviews:
        average_rating = sum(review.rating for review in movie.reviews) / len(movie.reviews)
        movie.average_rating = average_rating
    else:
        movie.average_rating = 0.0

    return movie


def update_movie(movie_id: int, movie: AddMovieForm, db: session):
    """
    This function updates a movie in the database by its id
    :return: Updated movie object
    """
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if db_movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with ID: {movie_id} not found!",
        )
    db_movie.description = movie.descr
    db_movie.cover_image_url = movie.image
    db_movie.length = movie.length
    db_movie.title = movie.title
    db.casts = movie.casts
    db.thriller = movie.thriller
    db.genre = movie.genre

    db.commit()
    db.refresh(db_movie)

    return db_movie


def delete_movie(movie_id: int, db: session):
    """
    Delete a movie from the database by it ID
    :param movie_id:
    :param db:
    :return: None
    """
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    print(db_movie.cover_image_url.split("/"))
    image_name = db_movie.cover_image_url.split("/")[1]

    if db_movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with ID: {movie_id} not found!",
        )

    delete_image(image_name)
    print(image_name)
    db.delete(db_movie)
    db.commit()

    """ END MOVIE OPERATIONS"""
