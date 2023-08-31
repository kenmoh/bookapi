from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
BASE_URL = 'http://localhost:8000/api/movies'
HEALTH_URL = 'https://bookapi-6soz.onrender.com'

data = {
    "title": "Why Ask Why",
    "length": 1.58,
    "description": "Action",
    "cover_image_url": "string.png",
    "casts": "Ramsey Noah Jr, Liz Benson",
}

update_data = {
    "title": "Snake and Tiger",
    "length": 2.58,
    "description": "Nollywood Movie",
    "cover_image_url": "string.png",
    "casts": "Zubi Michael, Kanayo O. Kanayo",
}

review_data = {
    "author": "Lee Sammy",
    "comment": "Testing",
    "rating": 3
}


def test_api_health():
    response = client.get(BASE_URL)
    assert response.status_code == status.HTTP_200_OK


def test_get_movies():
    response = client.get(BASE_URL)
    assert response.status_code == status.HTTP_200_OK


def test_add_movie():
    response = client.post(BASE_URL, json=data)
    assert response.status_code == status.HTTP_201_CREATED


def test_update_movie():
    response = client.put(f'{BASE_URL}/3', json=update_data)
    assert response.status_code == status.HTTP_202_ACCEPTED


def test_get_movie():
    """
    Test get book by ID
    :return: Book object
    """
    response = client.get(f'{BASE_URL}/3')
    assert response.status_code == status.HTTP_200_OK


def test_get_movie_reviews():
    """
    Get all reviews for a single book
    :return: List of reviews for a movie
    """
    response = client.get(f'{BASE_URL}/reviews/3')
    assert response.status_code == status.HTTP_200_OK


def test_add_movie_review():
    """
    Add review to a movie
    :return:  object
    """
    response = client.post(f'{BASE_URL}/reviews/3', json=review_data)
    assert response.status_code == status.HTTP_201_CREATED


def test_avg_movie_rating():
    """
    Get average rating of a movie
    :return: average rating
    """
    response = client.get(f'{BASE_URL}/average-rating/3')
    assert response.status_code == status.HTTP_200_OK


def test_delete_movie():
    response = client.delete(f'{BASE_URL}/7')
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_movie_review():
    response = client.delete(f'{BASE_URL}/reviews/11')
    assert response.status_code == status.HTTP_204_NO_CONTENT
