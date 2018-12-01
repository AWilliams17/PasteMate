import wtforms_json
from flask import Flask
from PasteMate.models import db
from PasteMate.api.routes import routes_bp, api
from PasteMate.api.jwt_loaders import jwt_manager
from os.path import exists

app = Flask(__name__, template_folder="../client/")
app.register_blueprint(routes_bp)
app.config.update(
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
    DEBUG=True
)

with app.app_context():
    db.init_app(app)
    if not exists(app.config['SQLALCHEMY_DATABASE_URI']):
        db.create_all()
    wtforms_json.init()

jwt_manager.init_app(app)
api.init_app(app)


if __name__ == '__main__':
    app.run(host='localhost')
