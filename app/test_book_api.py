from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
BASE_URL = 'http://127.0.0.1:5000/api/books'
HEALTH_URL = 'http://127.0.0.1:5000'

data = {
    'author': 'Sammy Lee',
    'title': 'Never Give Up',
    'description': 'From 10 men to victory',
    'isbn': 'ISBN2024'
}

update_data = {
    'author': 'Sammy Lee Yu',
    'title': 'Never Give Up...',
    'description': 'From 10 men to victory',
    'isbn': 'ISBN2024'
}

review_data = {
    "review_by": "Lee Sammy",
    "review_body": "Testing",
    "rating": 3
}


def test_api_health():
    response = client.get(BASE_URL)
    assert response.status_code == status.HTTP_200_OK


def test_get_books():
    response = client.get(BASE_URL)
    assert response.status_code == status.HTTP_200_OK


def test_add_book():
    response = client.post(BASE_URL, json=data)
    assert response.status_code == status.HTTP_201_CREATED


def test_update_book():
    response = client.put(f'{BASE_URL}/4', json=update_data)
    assert response.status_code == status.HTTP_202_ACCEPTED


def test_get_book():
    response = client.get(f'{BASE_URL}/4')
    assert response.status_code == status.HTTP_200_OK


def test_get_book_reviews():
    response = client.get(f'{BASE_URL}/reviews/4')
    assert response.status_code == status.HTTP_200_OK


def test_add_book_review():
    response = client.post(f'{BASE_URL}/reviews/4', json=review_data)
    assert response.status_code == status.HTTP_201_CREATED


def test_avg_book_rating():
    response = client.get(f'{BASE_URL}/average-rating/5')
    assert response.status_code == status.HTTP_200_OK
