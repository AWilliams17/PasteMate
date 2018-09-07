from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db
from flask_session import Session
from os import path

app = Flask(__name__, root_path="/server")
# SESSION_TYPE = 'redis'
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    "sqlite:///" + path.dirname(path.realpath(__file__)) + "\PM.db".replace('"\"', '\\')  # ugh

with app.app_context():
    db.init_app(app)

# Session(app)
app.debug = True

CORS(app)  # ToDo: Secure this. This allows CORS requests on all routes from any domain.


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


if __name__ == '__main__':
    # _session = Session()
    # _session.init_app(app)
    app.run()
