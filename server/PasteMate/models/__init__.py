from flask_sqlalchemy import SQLAlchemy
from PasteMate.config import app_config

db = SQLAlchemy()
# SECRET_KEY = app_config['SECRET_KEY']


# def password_encrypt(password):
#     return encrypt(SECRET_KEY, password)


# def password_decrypt(password):
#     return decrypt(SECRET_KEY, password)
