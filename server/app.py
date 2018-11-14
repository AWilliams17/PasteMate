"""
ToDo: Rate limit SignUp, SignIn, Paste Submit
"""


import wtforms_json
from api_resources import RegisterUser, LoginUser, RevokeAccess, RefreshUser, UserAuthStatus
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api
from models import RevokedToken
from flask_cors import CORS
from models import db
from os.path import exists
from datetime import timedelta

app = Flask(__name__, template_folder="../client/")
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///PM.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_PASSWORD_SALT'] = "12345"  # ToDo: Bad.
app.config['SECRET_KEY'] = "12345"  # ToDo: Bad.
app.config['CORS_SUPPORTS_CREDENTIALS'] = True
app.config['JWT_SECRET_KEY'] = '12345' # ToDo: Bad.
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)  # 7 days
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=14)  # 14 days
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_TOKEN_LOCATION'] = 'cookies'
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_ACCESS_COOKIE_PATH'] = '/auth/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/auth/refresh/'

with app.app_context():
    db.init_app(app)
    if not exists(app.config['SQLALCHEMY_DATABASE_URI']):
        db.create_all()
    wtforms_json.init()

app.debug = True

CORS(app)  # ToDo: Secure this. This allows CORS requests on all routes from any domain.

jwt_manager = JWTManager(app)
api = Api(app)


@jwt_manager.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedToken.is_jti_blacklisted(jti)


@jwt_manager.expired_token_loader
def expired_token_callback():
    return jsonify({'error': 'token_expired'}), 401


@jwt_manager.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'error': 'invalid_token'}), 401


@jwt_manager.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'error': 'authorization_required'}), 401


@jwt_manager.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({'error': 'fresh_token_required'}), 401


@jwt_manager.revoked_token_loader
def revoked_token_callback():
    return jsonify({'error': 'token_revoked'}), 401


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file('index.html')


api.add_resource(RegisterUser, '/api/user/register')
api.add_resource(LoginUser, '/api/user/login')
api.add_resource(RefreshUser, '/api/auth/refresh')
api.add_resource(UserAuthStatus, '/api/auth/status')
api.add_resource(RevokeAccess, '/api/auth/revoke')

if __name__ == '__main__':
    app.run(host='localhost')
