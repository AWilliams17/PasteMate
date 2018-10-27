"""
ToDo: Rate limit SignUp, SignIn, Paste Submit
ToDo: Test Refresh Tokens
ToDo: Encrypt the tokens
"""


import wtforms_json
from flask import Flask, jsonify, request, render_template
from flask_jwt_extended import (create_access_token,
    create_refresh_token, jwt_required, jwt_refresh_token_required,
    get_jwt_identity, get_raw_jwt, JWTManager)
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
app.config['JWT_SECRET_KEY'] = '12345' # ToDo: Bad.
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(7)  # 7 days
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(14)  # 14 days

with app.app_context():
    database_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    db.init_app(app)
    if not exists(database_path):
        db.create_all()
    wtforms_json.init()

# Session(app)
app.debug = True

CORS(app)  # ToDo: Secure this. This allows CORS requests on all routes from any domain.

jwt_manager = JWTManager(app)
parser = reqparse.RequestParser()
api = Api(app)

@jwt_manager.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedToken.is_jti_blacklisted(jti)


@api.resource('/sign_up')
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
        return {'success': True, 'access_token': access_token, 'refresh_token': refresh_token}


@api.resource('/invalidate_access')
class InvalidateAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()
        if 'jti' in jti:
            revoked_access_token = RevokedToken(jti=jti['jti'])
            revoked_access_token.save_to_db()
            return {'access_revoked': True}
        return {'access_revoked': False}


@api.resource('/invalidate_refresh')
class InvalidateRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()
        if 'jti' in jti:
            revoked_refresh_token = RevokedToken(jti=jti['jti'])
            revoked_refresh_token.save_to_db()
            return {'refresh_revoked': True}
        return {'refresh_revoked': False}


@api.resource('/refresh_user')
class RefreshUser(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


@api.resource('/current_user')
class GetCurrentUser(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        if current_user is None:
            return {'current_user': None}
        return {'current_user': current_user}


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
