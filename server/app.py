from flask import Flask, jsonify
from flask_cors import CORS
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, root_path="/server")
# SESSION_TYPE = 'redis'
app.config.from_object(__name__)
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
