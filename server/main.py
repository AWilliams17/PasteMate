"""
Contains initialization and instantiation of the flask app object,
along with initialization of extensions.
"""
import crython
import wtforms_json
from flask import Flask
from models import db
from models.paste import Paste
from api import api
from api.mail import async_mail
from api.jwt_loaders import jwt_manager
from os.path import exists

app = Flask('PasteMateApp', template_folder="../client/")
app.config.update(
    API_URL="http://localhost:5000/",
    SQLALCHEMY_DATABASE_URI="sqlite:///PM.db",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SECURITY_PASSWORD_SALT="12345",
    SECRET_KEY="12345",
    CORS_SUPPORTS_CREDENTIALS=True,
    JWT_SECRET_KEY="12345",
    JWT_BLACKLIST_ENABLED=True,
    JWT_BLACKLIST_TOKEN_CHECKS=['access', 'refresh'],
    JWT_COOKIE_CSRF_PROTECT=True,
    JWT_TOKEN_LOCATION="cookies",
    JWT_COOKIE_SECURE=False,
    MAIL_SERVER='',
    MAIL_PORT=587,
    MAIL_USE_TLS=False,
    MAIL_USERNAME='',
    MAIL_PASSWORD='',
    MAIL_DEFAULT_SENDER='',
    DEBUG=True
)

with app.app_context():
    db.init_app(app)
    if not exists(app.config['SQLALCHEMY_DATABASE_URI']):
        db.create_all()
    wtforms_json.init()

jwt_manager.init_app(app)
api.init_app(app)
async_mail.init_app(app)


@crython.job(hour='*/1')
def expire_pastes():
    with app.app_context():
        Paste.delete_expired_pastes()


if __name__ == '__main__':
    crython.start()
    app.run(host='localhost', use_reloader=False)
