from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    username = db.Column(db.String(24), unique=True, nullable=False)
    password = db.Column(db.String(128), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pastes = db.relationship('Paste', backref='submitter', order_by='Paste.id', lazy=True)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    def password_correct(self, password):
        return check_password_hash(self.password, password)

    def save_to_db(self):
        if self.find_by_email(self.email) is None and self.find_by_username(self.username) is None:
            db.session.add(self)
            db.session.commit()

    def to_dict(self):
        return dict(
            id=self.id,
            username=self.username,
            email=self.email,
            password=self.password,
            pastes=self.pastes
        )

    def __repr__(self):
        return '<Account %r>' % self.username

    def __init__(self, username, email, password, private):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password, method='sha256')
        self.private = private
        self.pastes = None


class Paste(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    title = db.Column(db.String(50), unique=False, nullable=False)
    language = db.Column(db.String(50), unique=False, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=True)
    content = db.Column(db.Text, unique=False, nullable=False)
    submission_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    edit_date = db.Column(db.DateTime, nullable=True)
    open_edit = db.Column(db.Boolean, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return dict(
            id=self.id,
            owner=self.owner_id,
            title=self.title,
            language=self.language,
            password=self.password,
            content=self.content,
            submission_date=self.submission_date,
            edit_date=self.edit_date,
            open_edit=self.open_edit,
            expiration_date=self.expiration_date
        )

    def __repr__(self):
        return '<Paste %r>' % self.title


class RevokedToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def save_to_db(self):
        if not self.is_jti_blacklisted(self.jti):
            db.session.add(self)
            db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
