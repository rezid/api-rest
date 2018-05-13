from db import db
from models.book_tag import book_tag_table


class BookModel(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13), nullable=False, unique=True)
    title = db.Column(db.String(255), nullable=False)
    authors = db.Column(db.String(255))
    cover = db.Column(db.String(1024))
    description = db.Column(db.String(1024))

    book_copie_list = db.relationship('BookCopieModel')

    tag_list = db.relationship("TagModel", secondary=book_tag_table)

    def __init__(self, isbn, title, authors, cover, description):
        self.isbn = isbn
        self.title = title
        self.authors = authors
        self.cover = cover
        self.description = description

    def json(self):
        return {
            'isbn': self.isbn,
            'title': self.title,
            'authors': self.authors,
            'cover': self.cover,
            'description': self.description,
            'tags': [x.json() for x in self.tag_list],
            'copies': [x.json() for x in self.book_copie_list]
        }

    @classmethod
    def find_by_isbn(cls, isbn):
        return cls.query.filter_by(isbn=isbn).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
