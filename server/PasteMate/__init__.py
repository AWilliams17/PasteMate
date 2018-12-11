"""
Contains initialization and instantiation of the flask app object,
along with initialization of extensions.
"""

import wtforms_json
from flask import Flask
from PasteMate.config import PasteMateConfig
from PasteMate.models import db
from PasteMate.api.routes import api
from PasteMate.api.jwt_loaders import jwt_manager
from os.path import exists


app = Flask(__name__, template_folder="../client/")
config = PasteMateConfig()
config.set_app_config(app)

with app.app_context():
    db.init_app(app)
    if not exists(app.config['SQLALCHEMY_DATABASE_URI']):
        db.create_all()
    wtforms_json.init()

jwt_manager.init_app(app)
api.init_app(app)

if __name__ == '__main__':
    app.run(host='localhost')
