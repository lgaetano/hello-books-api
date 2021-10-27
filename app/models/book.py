from app import db
# from author import Author

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    # author_id = db.Column(db.Integer, db.ForeignKey(Author.id), nullable=False)
    description = db.Column(db.String)

    def convert_dict(self):
        """Formats object attributes into dictionary."""
        return {
                "id": self.id,
                "title": self.title,
                "description": self.description
            }