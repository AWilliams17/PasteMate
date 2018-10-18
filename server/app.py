import wtforms_json
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_jwt_extended import (create_access_token,
    create_refresh_token, jwt_required, jwt_refresh_token_required,
    get_jwt_identity, get_raw_jwt, JWTManager)
from werkzeug.security import safe_str_cmp
from models import db, Account, Paste
from forms import RegistrationForm
from os.path import dirname, realpath, exists
app = Flask(__name__, template_folder="../client/")
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    "sqlite:///" + dirname(realpath(__file__)) + "\PM.db".replace('"\"', '\\')  # ugh
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_PASSWORD_SALT'] = "12345"  # ToDo: Bad.
app.config['SECRET_KEY'] = "12345"  # ToDo: Bad.
app.config['JWT_SECRET_KEY'] = '12345' # ToDo: Bad.

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
