from datetime import datetime
from db import db


class BookCopieModel(db.Model):
    __tablename__ = 'book_copie'

    id = db.Column(db.Integer, primary_key=True)

    contribution_date = db.Column(
        db.DateTime(timezone=True), default=datetime.utcnow)

    book_id = contributor_user_id = db.Column(db.Integer,
                                              db.ForeignKey('book.id'))
    book = db.relationship('BookModel')

    contributor_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    contributor_user = db.relationship('UserModel')

    borrower_list = db.relationship('BorrowModel')

    def __init__(self, book_id, contributor_user_id):
        self.book_id = book_id
        self.contributor_user_id = contributor_user_id

    def json(self):
        return {
            'copy_id': self.id,
            'book_isbn': self.book.isbn,
            'contribution_date': str(self.contribution_date),
            'contributor_user_email': self.contributor_user.email,
            'borowers': [x.json() for x in self.borrower_list]
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()