from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.book import BookModel


class Book(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="This field cannot be left blank!")
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="Every book needs a store id.")

    def get(self, isbn):
        try:
            book = BookModel.find_by_isbn(isbn)
        except:
            return {'message': 'An error occured searching the book.'}, 500
        if book:
            return book.json()
        return {'message': 'Book not found'}, 404

    @jwt_required()
    def post(self, isbn):
        if BookModel.find_by_isbn(isbn):
            return {
                'message': 'A book with isbn \'{}\' already exist'.format(isbn)
            }, 400
        data = Book.parser.parse_args()
        book = BookModel(isbn, **data)
        try:
            book.save_to_db()
        except:
            return {'message': 'An error occured inserting the book.'}, 500
        return book.json(), 201

    @jwt_required()
    def put(self, isbn):
        data = Book.parser.parse_args()
        book = BookModel.find_by_isbn(isbn)
        if book is None:
            book = BookModel(isbn, **data)
        else:
            book.name = data['name']
            book.name = data['store_id']
        try:
            book.save_to_db()
        except:
            return {
                'message': 'An error occured creating/updationg the book.'
            }, 500
        return book.json()

    @jwt_required()
    def delete(self, isbn):
        try:
            book = BookModel.find_by_isbn(isbn)
            if book:
                book.delete_from_db()
        except:
            return {'message': 'An error occured deleting the book.'}, 500
        return {'message': 'Book deleted'}


class BookList(Resource):
    def get(self):
        return {'books': [x.json() for x in BookModel.query.all()]}
