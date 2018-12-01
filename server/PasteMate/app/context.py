import wtforms_json
from PasteMate import flask_app
from PasteMate.db.models import db
from os.path import exists

with flask_app.app_context():
    db.init_app(flask_app)
    if not exists(flask_app.config['SQLALCHEMY_DATABASE_URI']):
        db.create_all()
    wtforms_json.init()
