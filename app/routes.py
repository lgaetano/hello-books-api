from app import db
from app.models.book import Book
from app.models.author import Author
from flask import Blueprint, abort, json, jsonify, make_response, request

books_bp = Blueprint("books", __name__, url_prefix="/books")
authors_bp = Blueprint("authors", __name__, url_prefix="/authors")


# def sanitize_data(input_data):
#     data_types = {
#         “name”: str, 
#         “breed”: str, 
#         “age”: int
#         }

#     for name, val_type in data_types.items():
#         try:
#             val = input_data[name]
#             type_test = val_type(val)
#         except Exception as e:
#             print(e)
#             raise abort(400, “bad data”)

#     return input_data


@books_bp.route("", methods=["GET"])
def get_books():
    title = request.args.get("title")
    if title:
        books = Book.query.filter_by(title=title)
    else:
        books = Book.query.all()
    
    if not books:
        return "No books in list", 404

    books_response = []
    for book in books:
        books_response.append(book.to_dict())
    
    return jsonify(books_response), 200


@books_bp.route("", methods=["POST"])
def post_books():
    form_data = request.get_json()
    if "title" not in form_data or "description" not in form_data:
        return make_response("Invalid request.", 400)
    
    new_book = Book(title=form_data["title"],
                    description=form_data["description"])
    
    db.session.add(new_book)
    db.session.commit()

    return jsonify(new_book.to_dict()), 201

@books_bp.route("/<book_id>", methods=["GET", "PUT", "PATCH", "DELETE"])
def handle_book(book_id):
    book = Book.query.get(book_id)
    if not book:
            return make_response("Book not found", 404)

    if request.method == "GET":
        return jsonify(book.to_dict()), 200

    elif request.method == "PATCH":
        form_data = request.get_json()
        book.update_from_dict(form_data)

        db.session.commit()
        return jsonify(f"Book #{book.id} updated successfully."), 200
    
    elif request.method == "PUT":
        # Get new data
        form_data = request.get_json()
        try:
            book.replace_from_dict(form_data)
        except ValueError:
            return jsonify("Invalid request.", 400)
    
        db.session.commit()
        return jsonify(f"Book #{book.id} updated successfully."), 201

        # Q: db.session.add() # Why is there no db.session add here?

    elif request.method == "DELETE":
        db.session.delete(book)
        db.session.commit()
        return jsonify(f"Book #{book.id} deleted successfully."), 200

    @authors_bp.route("", methods=["GET"])
    def get_authors():
        author_name = request.args.get("name")

        if author_name:
            authors = Author.query.filter_by(name=author_name)

        else:
            authors = Author.query.all()

        authors_response = [author.to_dict() for author in authors]
        return jsonify(authors_response), 200

    @authors_bp.route("", methods=["POST"])
    def post_authors():
        pass