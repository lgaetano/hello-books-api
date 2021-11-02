from app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship("Author", back_populates="book")

    COLUMNS = ["title", "description"]

    def to_dict(self):
        """Formats object attributes into dictionary."""
        return {
                "id": self.id,
                "title": self.title,
                "description": self.description
            }

    def replace_from_dict(self, data):
        for column in self.COLUMNS:
            if column in data:
                setattr(self, column, data[column])
            else:
                raise ValueError(f"Required column {column} missing.")

    def update_from_dict(self, data):
        for column in self.COLUMNS:
            if column in data:
                setattr(self, column, data[column])