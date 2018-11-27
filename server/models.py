from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4
db = SQLAlchemy()


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(256), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pastes = db.relationship('Paste', backref='submitter', order_by='Paste.id', lazy=True, uselist=False)

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
            pastes=self.pastes
        )

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password, method='sha256')
        self.pastes = None

    def __repr__(self):
        return '<Account %r>' % self.username


class Paste(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    title = db.Column(db.String(64), unique=False, nullable=False)
    language = db.Column(db.String(50), unique=False, nullable=False)
    password = db.Column(db.String(256), unique=False, nullable=True)
    content = db.Column(db.Text, unique=False, nullable=False)
    submission_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    edit_date = db.Column(db.DateTime, nullable=True)
    open_edit = db.Column(db.Boolean, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=True)
    paste_uuid = db.Column(db.Integer, unique=True, nullable=False)

    # This can probably be done in a better way
    expiration_options = {
        0: None,
        1: datetime.utcnow() + timedelta(minutes=10),
        2: datetime.utcnow() + timedelta(hours=1),
        3: datetime.utcnow() + timedelta(days=1),
        4: datetime.utcnow() + timedelta(weeks=1),
        5: datetime.utcnow() + timedelta(weeks=4),
        6: datetime.utcnow() + timedelta(weeks=26),
        7: datetime.utcnow() + timedelta(days=365)
    }

    def paste_dict(self):
        def strf_date(date): return date.strftime("%Y-%m-%d %H:%M:%S") if date is not None else None
        return {
            'title': self.title,
            'language': self.language,
            'content': self.content.splitlines(),
            'submission_date': strf_date(self.submission_date),
            'edit_date': strf_date(self.edit_date),
            'expiration_date': strf_date(self.expiration_date),
            'open_edit': self.open_edit,
            'owner_name': Account.find_by_id(self.owner_id).username,
            # If this paste has hit its expiration date, but the deletion job for it hasn't run yet, tell the client
            'deletion_inbound': datetime.utcnow() >= self.expiration_date if self.expiration_date is not None else False
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_uuid(cls, paste_uuid):
        return cls.query.filter_by(paste_uuid=paste_uuid).first()

    def password_correct(self, password):
        return check_password_hash(self.password, password)

    def __init__(self, owner_id, title, language, password, content, open_edit, expiration):
        self.owner_id = owner_id
        self.title = title
        self.language = language
        self.password = None
        if password is not None:
            self.password = generate_password_hash(password, method='sha256')
        self.content = content
        self.open_edit = open_edit
        self.expiration_date = self.expiration_options.get(expiration)
        self.paste_uuid = str(uuid4())[:8]

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
