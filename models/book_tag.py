from db import db

book_tag_table = db.Table('book_tag', db.Model.metadata,
                          db.Column('book_id', db.Integer,
                                    db.ForeignKey('book.id')),
                          db.Column('tag_id', db.Integer,
                                    db.ForeignKey('tag.id')))
