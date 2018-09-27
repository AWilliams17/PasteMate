from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from models import db, Account, Paste
from flask_session import Session
from os import path, scandir


app = Flask(__name__, template_folder="../client/")

# SESSION_TYPE = 'redis'
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    "sqlite:///" + path.dirname(path.realpath(__file__)) + "\PM.db".replace('"\"', '\\')  # ugh
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_PASSWORD_SALT'] = "12345"  # ToDo: Bad.
app.config['SECRET_KEY'] = "12345"  # ToDo: Bad.

with app.app_context():
    db.init_app(app)

# Session(app)
app.debug = True

CORS(app)  # ToDo: Secure this. This allows CORS requests on all routes from any domain.


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = Account(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


if __name__ == '__main__':
    # _session = Session()
    # _session.init_app(app)
    app.run()
