from fastapi import APIRouter, Depends, status, HTTPException
import requests
from sqlalchemy.orm import Session

from app.database import get_db
from app.forms import AddMovieForm
from app.schema.movie_schema import (
    MovieResponseSchema,
    ReviewResponseSchema,
    ReviewCreateSchema,
    AverageMovieReview,
)
from app.services import movie_services


movie_router = APIRouter(tags=["Movies"], prefix="/api/movies")
REVIEW_URL = "https://reviewapi.onrender.com/api/reviews"

""" START MOVIE ROUTE"""


@movie_router.get("", status_code=status.HTTP_200_OK)
def get_movies(db: Session = Depends(get_db)) -> list[MovieResponseSchema]:
    """
    Get all movies from the database
    :param db:
    :return: All Movies
    """
    return movie_services.get_all_movies(db)


@movie_router.post("", status_code=status.HTTP_201_CREATED)
def add_new_movie(
    movie: AddMovieForm = Depends(), db: Session = Depends(get_db)
) -> MovieResponseSchema:
    """
    Add new movie to the database
    """

    return movie_services.add_movie(movie, db)


@movie_router.put("/{movie_id}", status_code=status.HTTP_202_ACCEPTED)
def update_movie(
    movie_id, movie: AddMovieForm = Depends(), db: Session = Depends(get_db)
) -> MovieResponseSchema:
    """
    Update a movie by it ID
    """

    return movie_services.update_movie(movie_id, movie, db)


@movie_router.get("/{movie_id}", status_code=status.HTTP_200_OK)
def get_movie(movie_id, db: Session = Depends(get_db)) -> MovieResponseSchema:
    """
    Get a single movie from the database
    """

    return movie_services.get_movie(movie_id, db)


@movie_router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    """
    Delete a movie from database
    """
    requests.delete(f"{REVIEW_URL}/delete-reviews/{movie_id}")
    return movie_services.delete_movie(movie_id, db)


""" END MOVIE ROUTE """

""" START REVIEW ROUTE """

#
# @movie_router.get("/reviews/{movie_id}", status_code=status.HTTP_200_OK)
# def get_movie_reviews(movie_id: int) -> list[ReviewResponseSchema]:
#     """
#     Get all reviews by a movie
#     """
#     response = requests.get(f"{REVIEW_URL}/{movie_id}")
#     data = response.json()
#     return data
#
#
# @movie_router.post("/reviews/{movie_id}", status_code=status.HTTP_201_CREATED)
# def add_review(
#     movie_id: int, review: ReviewCreateSchema, db: Session = Depends(get_db)
# ) -> ReviewResponseSchema:
#     """
#     Add review to a movie
#     :param movie_id:
#     :param review:
#     :param db:
#     :return: New Review
#     """
#     movie = movie_services.get_movie(movie_id, db)
#     data = {"comment": review.comment, "author": review.author, "rating": review.rating}
#     if not movie:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Movie with ID: {movie_id} not found!",
#         )
#     response = requests.post(f"{REVIEW_URL}/{movie_id}", json=data)
#     data = response.json()
#     return data
#
#
# @movie_router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_review(review_id: int):
#     """
#     Delete movie review
#     :param review_id:
#     :return: None
#     """
#     response = requests.delete(f"{REVIEW_URL}/delete-review/{review_id}")
#     return response
#
#
# @movie_router.get("/average-rating/{movie_id}", status_code=status.HTTP_200_OK)
# def get_avg_movie_rating(movie_id: int) -> AverageMovieReview:
#     """
#     Get the average rating of a movie
#     :param movie_id:
#     :return: average movie rating (float)
#     """
#     response = requests.get(f"{REVIEW_URL}/average-rating/{movie_id}")
#     avg_rating = response.json()
#     return avg_rating


""" END REVIEW ROUTE """
