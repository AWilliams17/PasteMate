from PasteMate.models import db
from werkzeug.security import generate_password_hash, check_password_hash


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(256), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pastes = db.relationship('Paste', backref=db.backref('submitter', lazy='dynamic', uselist=True),
                             order_by='Paste.submission_date.desc()', lazy='dynamic')

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

    def update_password(self, password):
        self.password = generate_password_hash(password, method='sha256')
        db.session.commit()

    def update_email(self, email):
        if not self.find_by_email(self.email):
            self.email = email
            db.session.commit()

    def save_to_db(self):
        if not self.find_by_email(self.email) and not self.find_by_username(self.username):
            db.session.add(self)
            db.session.commit()

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password, method='sha256')

    def __repr__(self):
        return '<Account %r>' % self.username


