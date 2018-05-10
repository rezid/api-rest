from db import db

class BookModel(db.Model):
  __tablename__ = 'books'
  
  id = db.Column(db.Integer, primary_key=True)
  isbn = db.Column(db.String(80))
  name = db.Column(db.String(80))

  store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
  store = db.relationship('StoreModel')

  def __init__(self, isbn, name, store_id):
    self.isbn = isbn
    self.name = name
    self.store_id = store_id

  def json(self):
    return {'isbn': self.isbn, 'name': self.name}
  
  @classmethod
  def find_by_isbn(cls, isbn):
    return cls.query.filter_by(isbn=isbn).first()

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()