from flask import Blueprint, json, jsonify, request

class Book():
    def __init__(self, id, author, title, description):
        self.id = id
        self.author = author
        self.title = title
        self.description = description

class Author():
    def __init__(self, id, name, books):
        self.id = id
        self.name = name
        self.books = books

# book1 = Book(1, "Barry", "See Spot Run", "Timeless novel.")
# book2 = Book(2, "Nary", "Clifford the Big Red Dog", "Heartbreaking romance."),
# book3 = Book(1, "Barry", "See Spot Walk", "Timeless novel.")

# author1 = Author(1, "Barry", [book1, book3])
# author2 = Author(2, "Nary", ["Clifford the Big Red Dog", "Heartbreaking romance."])
# author3 = Author(3, "Mary", ["Epic Novel", "Big, Big book"])

# books = [book1, book2, book3]
# authors = [author1, author2, author3]

books = [
    Book(1, "Barry", "See Spot Run", "Timeless novel."),
    Book(2, "Nary", "Clifford the Big Red Dog", "Heartbreaking romance."),
    Book(1, "Barry", "See Spot Walk", "Timeless novel.")
]
authors = [
    Author(1, "Barry", ["See Spot Run", "See Spot Walk"]),
    Author(2, "Nary", ["Clifford the Big Red Dog", "Heartbreaking romance."]),
    Author(3, "Mary", ["Epic Novel", "Big, Big book"])
]

books_bp = Blueprint("books", __name__, url_prefix="/books")
authors_bp = Blueprint("authors", __name__, url_prefix="/authors")

@books_bp.route("", methods=["GET"])
def handle_books():
    books_response = []
    for book in books:
        books_response.append({
            "id": book.id,
            "author": book.author,
            "title": book.title,
            "description": book.description
        })

    return jsonify(books_response)

@books_bp.route("/<book_id>", methods=["GET"])
def handle_book(book_id):
    book_id = int(book_id)
    for book in books:
        print(book.id)
        if book.id == book_id:
            return {
                "id": book.id,
                "author": book.author,
                "title": book.title,
                "description": book.description
            }
    return {
        "error": "Book id for this number doesn't exist."
    }, 404

@authors_bp.route("", methods=["GET"])
def handle_authors():
    author_list = []

    for author in authors:
        author_list.append({
            "id": author.id, 
            "name": author.name,
            "books": author.books
        })
    return jsonify(author_list)

@authors_bp.route("/<author_id>", methods={"GET", "POST"})
def handle_author(author_id):
    if request.method == "GET":
        author_id = int(author_id)
        for author in authors:
            if author_id == author.id:
                return {
                    "id": author.id,
                    "name": author.name,
                    "books": author.books
                }
            else:
                return {
                    "error": "No author with this id exists."
                }

    elif request.method == "POST":
        pass














hello_world_bp = Blueprint("hello_world", __name__)


@hello_world_bp.route("/hello-world", methods=["GET"])
def say_hello_world():
    body = "Hello, World!"
    return body


@hello_world_bp.route("/hello/JSON", methods=["GET"])
def hello_JSON():
    return {
                "name": "Ada Lovelace",
                "message": "Hello!",
                "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
            }, 200

@hello_world_bp.route("/broken-endpoint-with-broken-server-code", methods=["GET"])
def broken_endpoint():
    response_body = {
        "name": "Ada Lovelace",
        "message": "Hello!",
        "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
    }
    new_hobby = "Surfing"
    response_body["hobbies"].append(new_hobby)
    return response_body

