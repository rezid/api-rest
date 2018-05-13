from db import db
from models.book_tag import book_tag_table


class TagModel(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    book_list = db.relationship(
        "BookModel", secondary=book_tag_table, back_populates="tag_list")

    def __init__(self, name):
        self.name = name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {'name': self.name}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_isbn_and_name(cls, isbn, name):
        return TagModel.query.filter(
            TagModel.book_list.any(isbn=isbn)).filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
