from app import db
from app.models.book import Book
from app.models.author import Author
from app.models.genre import Genre
from flask import Blueprint, abort, json, jsonify, make_response, request

books_bp = Blueprint("books", __name__, url_prefix="/books")
authors_bp = Blueprint("authors", __name__, url_prefix="/authors")
genres_bp = Blueprint("genres", __name__, url_prefix="/genres")

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

# BOOKS ---------------------
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

# BOOK ID ---------------------
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

# AUTHORS ---------------------
@authors_bp.route("", methods=["GET", "POST"])
def handle_authors():
    if request.method == "GET":
        authors = Author.query.all()

        # authors_response = [author.to_dict() for author in authors]
        authors_response = []
        for author in authors:
            authors_response.append(author.to_dict())

        return jsonify(authors_response), 200
    
    elif request.method == "POST":
        form_data = request.get_json()

        new_author = Author(
            name=form_data["name"]
        )

        db.session.add(new_author)
        db.session.commit()

        return make_response(f"{new_author.name} successfully created", 201)

# AUTHOR/BOOKS ---------------------
@authors_bp.route("/<author_id>/books", methods=["GET", "POST"])
def get_authors_nested(author_id):
    author = Author.query.get(author_id)
    if author is None:
        return make_response("Author not found", 404)

    if request.method == "GET":
        author_name = request.args.get("name")

        if author_name:
            author = Author.query.filter_by(name=author_name)

        else:
            author = Author.query.get(author_id)

        books_response = [book.to_dict() for book in author.books]
        return jsonify(books_response), 200
    
    if request.method == "POST":
        form_data = request.get_json()
        new_book = Book(
            title=form_data["title"],
            description=form_data["description"],
            author=author
        )

        db.session.add(new_book)
        db.session.commit()

        return make_response(f"{new_book.title} by {new_book.author.name} successfully created", 201)

# GENRES ---------------------
@genres_bp.route("", methods=["GET", "POST"])
def handle_genres():
    if request.method == "GET":
        genres = Genre.query.all()
        
        if not genres:
            return "No genre found", 404

        genre_response = []
        for genre in genres:
            genre_response.append({
                "name": genre.name
            })
    

    elif request.method == "POST":
        form_data = request.get_json()

        new_genre = Genre(name=form_data["name"])
        db.session.add(new_genre)
        db.session.commit()

        return jsonify(f"Successfully added {new_genre.name}"), 201

# BOOKS/GENRES ---------------------
@genres_bp.route("/books/<book_id>/assign_genres", methonds=["PATCH"])
def assign_genres(book_id):
    # Query for book_id
    book = Book.query.get(book_id)
    if not book:
        return jsonify("No book found"), 404

    form_data = request.get_json()
        # {"genres": [1, 2, 3]}

    for id in form_data["genres"]:
        book.genres.append(Genre.query.get(id))

    db.session.commit()

    return jsonify("Genre successfully added"), 200
