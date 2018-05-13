from datetime import datetime
from db import db


class BorrowModel(db.Model):
    __tablename__ = 'borrow'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    end_date = db.Column(db.DateTime(timezone=True))

    book_copie_id = db.Column(db.Integer, db.ForeignKey('book_copie.id'))
    book_copie = db.relationship('BookCopieModel')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('UserModel')

    def __init__(self, end_date, book_copie_id, user_id):
        self.end_date = end_date
        self.book_copie_id = book_copie_id
        self.user_id = user_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            'book_copie_id': self.book_copie_id,
            'user_email': self.user.email,
            'start_date': str(self.start_date),
            'end_date': str(self.end_date)
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_book_copie_id_and_end_date(cls, book_copie_id, end_date):
        return cls.query.filter_by(
            book_copie_id=book_copie_id, end_date=end_date).first()

    @classmethod
    def find_by_book_copie_id_and_user_id_and_end_date(cls, book_copie_id,
                                                       user_id, end_date):
        return cls.query.filter_by(
            book_copie_id=book_copie_id, user_id=user_id,
            end_date=end_date).first()
