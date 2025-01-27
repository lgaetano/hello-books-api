from app import db

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    books = db.relationship("Book", back_populates="author")

    def to_dict(self):
        """Formats object attributes into dictionary."""
        return {
                "id": self.id,
                "name": self.name,
                "books": [book.title for book in self.books]
            }