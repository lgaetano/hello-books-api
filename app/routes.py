from app import db
from app.models.book import Book
from flask import Blueprint, json, jsonify, make_response, request

books_bp = Blueprint("books", __name__, url_prefix="/books")
authors_bp = Blueprint("authors", __name__, url_prefix="/authors")

@books_bp.route("", methods=["GET", "POST"])
def handle_books():
    if request.method == "GET":
        books = Book.query.all()
        if not books:
            return "No books in list", 404

        books_response = []

        for book in books:
            books_response.append({
                "id": book.id,
                "title": book.title,
                "description": book.description
            })
        return jsonify(books_response), 200


    elif request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body:
            return make_response("Invalid request.", 400)
        
        new_book = Book(title=request_body["title"],
                        description=request_body["description"])

        db.session.add(new_book)
        db.session.commit()

        return make_response(f"Book {new_book.title} successfully created",
                            201)

@books_bp.route("/<book_id>", methods=["GET", "PUT", "DELETE"])
def handle_book(book_id):
    book_id = int(book_id)
    book = Book.query.get(book_id)
    if not book:
            return "Book not found", 404

    if request.method == "GET":
        return make_response({
            "id": book.id,
            "title": book.title,
            "description": book.description
        }, 200)
    
    elif request.method == "PUT":
        # Get new data
        request_body = request.get_json()

        if ("title" not in request_body) or ("description" not in request_body):
            return make_response("Invalid request.", 400)
        
        book.title=request_body["title"]
        book.description=request_body["description"]
    
        db.session.commit()

        return make_response(
            f"Book #{book.id} successfully updated.", 201
            )

        # Q: db.session.add() # Why is there no db.session add here?

    elif request.method == "DELETE":
        db.session.delete(book)
        db.session.commit()
        return make_response(f"Book #{book.id} successfully deleted", 200)