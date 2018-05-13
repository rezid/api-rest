from datetime import datetime
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.book import BookModel
from models.book_copie import BookCopieModel
from models.borrow import BorrowModel
from models.tag import TagModel


class BookList(Resource):
    def get(self):
        return {'books': [x.json() for x in BookModel.query.all()]}


class Book(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'title',
        type=str,
        required=True,
        help="This field cannot be left blank!")
    parser.add_argument('authors', type=str, required=False)
    parser.add_argument('cover', type=str, required=False)
    parser.add_argument('description', type=str, required=False)

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
            book.title = data['title']
            book.authors = data['authors']
            book.description = data['description']
            book.cover = data['cover']
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


class TagList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="This field cannot be left blank!")

    def get(self, isbn):
        book = BookModel.find_by_isbn(isbn)
        if book:
            return {'tags': [x.json() for x in book.tag_list]}
        return {'message': 'Book not found'}, 404

    @jwt_required()
    def post(self, isbn):
        try:
            book = BookModel.find_by_isbn(isbn)
            if book is None:
                return {'message': 'Book not found'}, 404
            data = TagList.parser.parse_args()
            tagName = data['name'].lower()
            tag = TagModel.find_by_name(tagName)
            if tag is None:
                tag = TagModel(tagName)
                tag.save_to_db()
            else:
                if TagModel.find_by_isbn_and_name(isbn, tagName):
                    return {'message': 'the tag already added'}, 400
            book.tag_list.append(tag)
            book.save_to_db()
        except:
            return {'message': 'An error occured.'}, 500
        return {'tag': tag.json()}


class Tag(Resource):
    @jwt_required()
    def delete(self, isbn, name):
        try:
            book = BookModel.find_by_isbn(isbn)
            if book is None:
                return {'message': 'Book not found'}, 404
            tag = TagModel.find_by_name(name)
            if tag in book.tag_list:
                book.tag_list.remove(tag)
            book.save_to_db()
        except:
            return {'message': 'An error occured in the server.'}, 500
        return {'message': 'Tag deleted from book'}


class BookCopieList(Resource):
    def get(self, isbn):
        book = BookModel.find_by_isbn(isbn)
        if book:
            return {'copies': [x.json() for x in book.book_copie_list]}
        return {'message': 'Book not found'}, 404

    @jwt_required()
    def post(self, isbn):
        try:
            book = BookModel.find_by_isbn(isbn)
            if book is None:
                return {'message': 'Book not found'}, 404

            book_copie = BookCopieModel(book.id, current_identity.id)
            book_copie.save_to_db()
        except:
            return {'message': 'An error occured in the server.'}, 500
        return book_copie.json(), 201


class BookCopie(Resource):
    def get(self, id):
        try:
            book_copie = BookCopieModel.find_by_id(id)
            if book_copie is None:
                return {'message': 'Book Copie not found'}, 404
        except:
            return {'message': 'An error occured in the server.'}, 500
        return book_copie.json()

    @jwt_required()
    def delete(self, id):
        try:
            book_copie = BookCopieModel.find_by_id(id)
            if book_copie:
                book_copie.delete_from_db()
        except:
            return {'message': 'An error occured in the server.'}, 500
        return {'message': 'Book Copie deleted'}


class BorrowList(Resource):
    def get(self, id):
        try:
            book_copie = BookCopieModel.find_by_id(id)
            if book_copie is None:
                return {'message': 'Book Copie not found'}, 404
        except:
            return {'message': 'An error occured in the server.'}, 500
        return {'borrows': [x.json() for x in book_copie.borrower_list]}

    @jwt_required()
    def post(self, id):
        try:
            book_copie = BookCopieModel.find_by_id(id)
            if book_copie is None:
                return {'message': 'Book Copie not found'}, 404
            if BorrowModel.find_by_book_copie_id_and_end_date(
                    book_copie.id, None):
                return {'message': 'Book already borrowed'}, 400
            borrow = BorrowModel(None, book_copie.id, current_identity.id)
            borrow.save_to_db()
        except:
            return {'message': 'An error occured in the server.'}, 500
        return borrow.json(), 201


class ReturnList(Resource):
    @jwt_required()
    def post(self, id):
        try:
            book_copie = BookCopieModel.find_by_id(id)
            if book_copie is None:
                return {'message': 'Book Copie not found'}, 404
            borrow = BorrowModel.find_by_book_copie_id_and_user_id_and_end_date(
                book_copie.id, current_identity.id, None)
            if borrow is None:
                return {'message': 'You have not borrowed this book'}, 400
            borrow.end_date = datetime.utcnow()
            borrow.save_to_db()
        except:
            return {'message': 'An error occured in the server.'}, 500
        return borrow.json(), 201
