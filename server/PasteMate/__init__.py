from flask import Flask

flask_app = Flask(__name__, template_folder="../client/")

from PasteMate.app import config, context, jwt_loaders
from PasteMate.db import models
from PasteMate.api import forms, resources, routes

if __name__ == '__main__':
    flask_app.run(host='localhost')
