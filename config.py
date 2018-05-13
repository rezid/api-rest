import os
from datetime import timedelta

SECRET_KEY = b'zidane'

# When debug = Flase in the flask application, and We make a call to a jwt
# protected endpoint without an access token the process will terminate with
# 500 Internal Server Error without this config
PROPAGATE_EXCEPTIONS = True

# change the default url to the authentication endpoint
JWT_AUTH_URL_RULE = '/login'

# config JWT to expire within 1 year
JWT_EXPIRATION_DELTA = timedelta(days=365)

# config JWT auth key name to be 'email' instead of default 'username'
JWT_AUTH_USERNAME_KEY = 'email'

# desactivate FLASK SQLALCHEMY track modification
SQLALCHEMY_TRACK_MODIFICATIONS = False
# select the db used
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///data.db')

# Google Oauth 2.0
# https://developers.google.com/identity/protocols/OpenIDConnect#prompt
GOOGLE_CLIENT_ID = '1056568337695-1kh870neuo84h5pjv23krgsfgsq51mdv.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'npLt4bLPhHWiSlosidGfWVVf'
GOOGLE_CLIENT_KWARGS = {
    'scope': 'openid email profile',
    'prompt': 'select_account'
}