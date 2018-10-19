"""
ToDo: Lots of refactoring here.
ToDo: Rate limit SignUp, SignIn, Paste Submit
ToDo: Test Refresh Tokens
"""


import wtforms_json
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_jwt_extended import (create_access_token,
    create_refresh_token, jwt_required, jwt_refresh_token_required,
    get_jwt_identity, get_raw_jwt, JWTManager)
from werkzeug.security import safe_str_cmp
from models import db, Account, Paste, RevokedToken
from forms import RegistrationForm
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
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(7)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(14)

jwt = JWTManager(app)

with app.app_context():
    database_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    db.init_app(app)
    if not exists(database_path):
        db.create_all()
    wtforms_json.init()

# Session(app)
app.debug = True

CORS(app)  # ToDo: Secure this. This allows CORS requests on all routes from any domain.

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedToken.is_jti_blacklisted(jti)

@app.route('/sign_up', methods=['POST'])
def register():
    data = request.get_json()
    form = RegistrationForm.from_json(data)
    if not form.validate():
        error_response = {'success': False, 'errors': form.errors}
        print(form.errors['username'])
        return jsonify(error_response)
    # user = Account(**data)
    # user.save_to_db()
    access_token = create_access_token(identity=data['username'], fresh=True)
    refresh_token = create_refresh_token(identity=data['username'])
    success_response = {'success': True, 'access_token': access_token, 'refresh_token': refresh_token}
    return jsonify(success_response), 201


@app.route('/invalidate_access')
@jwt_required
def invalidate_access():
    jti = get_raw_jwt()
    if 'jti' in jti:
        revoked_access_token = RevokedToken(jti=jti['jti'])
        revoked_access_token.save_to_db()
    return jsonify(True), 201


@app.route('/invalidate_refresh')
@jwt_refresh_token_required
def invalidate_refresh():
    jti = get_raw_jwt()
    if 'jti' in jti:
        revoked_refresh_token = RevokedToken(jti=jti['jti'])
        revoked_refresh_token.save_to_db()
    return jsonify(True), 201


@app.route('/refresh_user', methods=['POST'])
@jwt_refresh_token_required
def renew_token():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity = current_user)
    return {'access_token': access_token}


@app.route('/get_login')
@jwt_required
def get_login():
    current_user = get_jwt_identity()
    if current_user is None:
        print(current_user)
        return jsonify("Not logged in."), 200
    return jsonify(current_user), 200


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
