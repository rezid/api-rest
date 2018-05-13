import sqlite3
from db import db


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    familiy_name = db.Column(db.String(80))
    given_name = db.Column(db.String(80))
    picture = db.Column(db.String(2083))
    password = db.Column(db.String(2048), nullable=False)

    def __init__(self, email, familiy_name, given_name, picture, password):
        self.email = email
        self.familiy_name = familiy_name
        self.given_name = given_name
        self.picture = picture
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            'email': self.email,
            'familiy_name': self.familiy_name,
            'given_name': self.given_name,
            'picture': self.picture,
            'password': self.password
        }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
