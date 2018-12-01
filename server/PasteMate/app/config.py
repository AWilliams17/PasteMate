from PasteMate import flask_app
from flask_cors import CORS

flask_app.config.from_object(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///PM.db"
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
flask_app.config['SECURITY_PASSWORD_SALT'] = "12345"  # ToDo: Bad.
flask_app.config['SECRET_KEY'] = "12345"  # ToDo: Bad.
flask_app.config['CORS_SUPPORTS_CREDENTIALS'] = True
flask_app.config['JWT_SECRET_KEY'] = '12345'  # ToDo: Bad.
flask_app.config['JWT_BLACKLIST_ENABLED'] = True
flask_app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
flask_app.config['JWT_COOKIE_CSRF_PROTECT'] = True
flask_app.config['JWT_TOKEN_LOCATION'] = 'cookies'
flask_app.config['JWT_COOKIE_SECURE'] = False  # TODO: This needs to be set to True after enabling HTTPS

flask_app.debug = True

CORS(flask_app)
