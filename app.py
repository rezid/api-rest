from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT

from authlib.flask.client import OAuth
from loginpass import create_flask_blueprint
from loginpass import Google

from security import authenticate, identity
from resources.user import handle_authorize
from resources.book import Book, BookList, BookCopie, BookCopieList, BorrowList, ReturnList, Tag, TagList

app = Flask(__name__)
app.config.from_pyfile('config.py')
oauth = OAuth(app)
api = Api(app)
jwt = JWT(app, authenticate, identity)

api.add_resource(BookList, '/books')
api.add_resource(Book, '/books/<string:isbn>')
api.add_resource(TagList, '/books/<string:isbn>/tags')
api.add_resource(Tag, '/books/<string:isbn>/tags/<string:name>')
api.add_resource(BookCopieList, '/books/<string:isbn>/copies')
api.add_resource(BookCopie, '/copies/<int:id>')
api.add_resource(BorrowList, '/copies/<int:id>/borrows')
api.add_resource(ReturnList, '/copies/<int:id>/returns')

# TODO: custom create_flask_blueprint with try catch
# visit:    /google/login
# callback: /google/auth
google_bp = create_flask_blueprint(Google, oauth, handle_authorize)
app.register_blueprint(google_bp, url_prefix='/google')

if __name__ == '__main__':
    from db import db

    @app.before_first_request
    def create_table():
        db.create_all()

    db.init_app(app)
    app.run(port=5000, debug=True)
