from flask.wrappers import Response
from app.models.book import Book
import copy

def test_get_all_books_with_no_records(client):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == None

def test_get_book_by_id(client, two_saved_books):
    # Act
    response = client.get('/books/1')
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Ocean Book",
        "description": "Watttttterrrrr"
    }

def test_post_book(client):
    # Act
    response = client.post("/books", json={
        "id": 1,
        "title": "Ocean Book",
        "description": "Watttttterrrrr"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body["title"] == "Ocean Book"
    assert response_body["description"] == "Watttttterrrrr"

    new_book = Book.query.get(1)
    assert new_book
    assert new_book.title == "Ocean Book"
    assert new_book.description == "Watttttterrrrr"

def test_post_dog_with_incomplete_data(client):
    request_body = {
        "title": "Ocean Book",
        "description": "Watttttterrrrr"
    }

    for key in request_body:
        incomplete_request_body = copy.copy(request_body)
        incomplete_request_body.pop(key)
        response = client.post("/books", json=incomplete_request_body)

        response_body = response.get_json()

        assert response.status_code == 400
        assert response_body == "Book not found"

    assert Book.query.all() == []