from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    username = db.Column(db.String(24), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pastes = db.relationship('Paste', backref='account', order_by='paste.id', cascade="all, delete-orphan", lazy=True)
    private = db.Column(db.Boolean, nullable=True)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)

    @classmethod
    def authenticate(cls, **kwargs):
        username = kwargs.get('username')
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not username or not email or not password:
            return None

        user = cls.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    def to_dict(self):
        return dict(id=self.id, username=self.username)

    def __repr__(self):
        return '<Account %r>' % self.username

    def __init__(self, username, email, password, private):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password, method='sha256')
        self.private = private
        self.pastes = None
        self.confirmed = False


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
