"""
ToDo: Rate limit SignUp, SignIn, Paste Submit
ToDo: Test Refresh Tokens
ToDo: Encrypt the tokens
"""


import wtforms_json
from flask import Flask, after_this_request, jsonify
from flask_jwt_extended import (create_access_token,
    create_refresh_token, jwt_required, jwt_refresh_token_required,
    get_jwt_identity, get_raw_jwt, JWTManager, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies)
from flask_restful import Resource, Api, reqparse
from forms import RegistrationForm
from models import RevokedToken
from flask_cors import CORS
from models import db
from os.path import dirname, realpath, exists
from datetime import timedelta

app = Flask(__name__, template_folder="../client/")
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    "sqlite:///" + dirname(realpath(__file__)) + "\PM.db".replace('"\"', '\\')  # ugh
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_PASSWORD_SALT'] = "12345"  # ToDo: Bad.
app.config['SECRET_KEY'] = "12345"  # ToDo: Bad.
app.config['CORS_SUPPORTS_CREDENTIALS'] = True
app.config['JWT_SECRET_KEY'] = '12345' # ToDo: Bad.
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(7)  # 7 days
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(14)  # 14 days
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_TOKEN_LOCATION'] = 'cookies'
app.config['JWT_ACCESS_COOKIE_PATH'] = '/auth/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/auth/refresh/'

with app.app_context():
    database_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    db.init_app(app)
    if not exists(database_path):
        db.create_all()
    wtforms_json.init()

app.debug = True

CORS(app)  # ToDo: Secure this. This allows CORS requests on all routes from any domain.

jwt_manager = JWTManager(app)
parser = reqparse.RequestParser()
api = Api(app)

@jwt_manager.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedToken.is_jti_blacklisted(jti)


@api.resource('/api/sign_up/')
class RegisterUser(Resource):
    def post(self):
        parser.add_argument('username')
        parser.add_argument('password')
        parser.add_argument('email')
        data = parser.parse_args()
        form = RegistrationForm.from_json(data)
        if not form.validate():
            return {'success': False, 'errors': form.errors}, 500
        # user = Account(**data)
        # user.save_to_db()
        access_token = create_access_token(identity=data['username'], fresh=True)
        refresh_token = create_refresh_token(identity=data['username'])
        @after_this_request
        def set_jwt_cookies(response):
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            return response
        return {'success': True, 'errors': None}, 200

@api.resource('/auth/revoke/')
class RevokeAccess(Resource):
    @jwt_required
    def get(self):
        @after_this_request
        def revoke_access(response):
            jti = get_raw_jwt()
            revoked_token = RevokedToken(jti=jti['jti'])
            revoked_token.save_to_db()
            unset_jwt_cookies(response)
            return response, 200

        return {'token_revoked': True}, 200


@api.resource('/auth/refresh/')
class RefreshUser(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        response = {'refreshed': True}
        set_access_cookies(response, access_token)
        return response


@api.resource('/auth/status/')
class GetLoginStatus(Resource):
    @jwt_required
    def get(self):
        return {'logged_in': True}  # If they aren't authenticated, @jwt_required automatically returned 401


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(host='localhost')
