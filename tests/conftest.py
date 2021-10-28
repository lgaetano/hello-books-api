import pytest
from app import create_app
from app import db
from app.models.book import Book

@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    with app.app_context(): # Designates application context --> dev/test
        db.create_all() # Re-creates tables from model at start of each test
        yield app # Returns app for use in test/fixtures
    
    # This runs after test using app has been completed
    with app. app_context():
        db.drop_all() # Drops all tables/deletes all data used in test

@pytest.fixture()
def client(app): # Requests "app" fixture to run, first
    return app.test_client() # Makes a test client, an object that simulates
                                # a client making HTTP request

## In our tests we will use "client" to send HTTP requests!

@pytest.fixture
def two_saved_books(app):
    # Arrange
    ocean_book = Book(title="Ocean Book",
                        description="Watttttterrrrr")
    mountain_book = Book(title="Mountain Book",
                        description="Cliffs")

    db.session.add_all([ocean_book, mountain_book])
    db.session.commit()