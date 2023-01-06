# SPDX-FileCopyrightText: 2023-present Heitor Pascoal de Bittencourt <heitorpbittencourt@gmail.com>
#
# SPDX-License-Identifier: MIT

from fastapi.testclient import TestClient

from isbn_api.config import Settings
from isbn_api.main import app, get_settings


client = TestClient(app)


# Test / endpoint

def get_settings_override():
    return Settings(server_name="test")


app.dependency_overrides[get_settings] = get_settings_override


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from server test"}


# Tests for /books/<ISBN> endpoint

def test_invalid_isbn_because_too_short():
    response = client.get("/books/123")
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "ensure this value has at least 10 characters" # noqa


def test_invalid_isbn_because_too_long():
    response = client.get("/books/12345678901234567890")
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "ensure this value has at most 13 characters" # noqa


def test_invalid_isbn_with_invalid_regex():
    response = client.get("/books/12345678901")
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == r'string does not match regex "^(\d{10}|\d{13})$"' # noqa


def test_invalid_isbn_inexistent():
    response = client.get("/books/9780140328722")
    assert response.status_code == 404
    assert response.json() == {"message": "ISBN 9780140328722 not found"}


def test_valid_isbn13():
    response = client.get("/books/9780140328721")
    assert response.status_code == 200
    assert response.json() == {"title": "Fantastic Mr. Fox",
                               "isbn10": ["0140328726"],
                               "isbn13": ["9780140328721"],
                               "authors": ["Roald Dahl"],
                               "cover_url": "https://covers.openlibrary.org/b/id/8739161-M.jpg"} # noqa


def test_valid_isbn10():
    response = client.get("/books/0140328726")
    assert response.status_code == 200
    assert response.json() == {"title": "Fantastic Mr. Fox",
                               "isbn10": ["0140328726"],
                               "isbn13": ["9780140328721"],
                               "authors": ["Roald Dahl"],
                               "cover_url": "https://covers.openlibrary.org/b/id/8739161-M.jpg"} # noqa


def test_valid_isbn10_alices_adventures():
    response = client.get("/books/1503222683")
    assert response.status_code == 200
    assert response.json() == {"title": "Alice's Adventures in Wonderland",
                               "isbn10": ["1503222683"],
                               "isbn13": ["9781503222687"],
                               "authors": ["Lewis Carroll"],
                               "cover_url": "https://covers.openlibrary.org/b/id/10476757-M.jpg"} # noqa
