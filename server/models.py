from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pastes = db.relationship('Paste', backref='account', lazy=True)

    def __repr__(self):
        return '<Account %r>' % self.username


class Paste(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    title = db.Column(db.String(50), unique=False, nullable=False)
    language = db.Column(db.String(50), unique=False, nullable=False)
    content = db.Column(db.Text, unique=False, nullable=False)
    submission_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    edit_date = db.Column(db.DateTime, nullable=True)
    open_edit = db.Column(db.Boolean, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Paste %r>' % self.title
