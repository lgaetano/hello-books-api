import pytest
from app import create_app
from app import db
from app.routes import Book

def test_book_class():
    book = Book(4, "Ovid", "Metamorphoses", "Roman mythology.")

    assert book.id == 4
    assert book.author == "Ovid"
    assert book.title == "Metamorphoses"
    assert book.description == "Roman mythology."
