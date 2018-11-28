"""
ToDo: Rate limit SignUp, SignIn, Paste Submit
"""


import wtforms_json
from api_resources import RegisterUser, LoginUser, RevokeAccess, RefreshUser, CurrentUser, SubmitPaste, \
    ViewPaste, PasteList, EditPaste
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from flask_restful import Api
from models import RevokedToken
from flask_cors import CORS
from models import db
from os.path import exists

app = Flask(__name__, template_folder="../client/")
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///PM.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_PASSWORD_SALT'] = "12345"  # ToDo: Bad.
app.config['SECRET_KEY'] = "12345"  # ToDo: Bad.
app.config['CORS_SUPPORTS_CREDENTIALS'] = True
app.config['JWT_SECRET_KEY'] = '12345'  # ToDo: Bad.
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_TOKEN_LOCATION'] = 'cookies'
app.config['JWT_COOKIE_SECURE'] = False  # TODO: This needs to be set to True after enabling HTTPS

with app.app_context():
    db.init_app(app)
    if not exists(app.config['SQLALCHEMY_DATABASE_URI']):
        db.create_all()
    wtforms_json.init()

app.debug = True

CORS(app)

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
api.add_resource(CurrentUser, '/api/auth/current_user')
api.add_resource(RevokeAccess, '/api/auth/revoke')
api.add_resource(SubmitPaste, '/api/paste/submit')
api.add_resource(ViewPaste, '/api/paste/view/<string:paste_uuid>')
api.add_resource(EditPaste, '/api/paste/edit/<string:paste_uuid>')
api.add_resource(PasteList, '/api/paste/list/<string:page>')

if __name__ == '__main__':
    app.run(host='localhost')
