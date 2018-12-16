from PasteMate.models import db
from PasteMate.models.account import Account
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from uuid import uuid4


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
        }

    def update_paste(self, title, language, content, open_edit, expiration, change_owner_fields=False):
        self.title = title
        self.language = language
        self.content = content
        self.edit_date = datetime.utcnow()
        # Check if the open edit, and expiration dates are going to be updated and do so if they are.
        # Otherwise, keep them all the same.
        if change_owner_fields:
            self.open_edit = self.open_edit if open_edit is None else (open_edit == 'true')
            self.expiration_date = self.expiration_date if not expiration else self.expiration_options.get(expiration)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_uuid(cls, paste_uuid):
        return cls.query.filter_by(paste_uuid=paste_uuid).first()

    @classmethod
    def delete_expired_pastes(cls):
        current_time = datetime.utcnow()
        expired_pastes = cls.query.filter(current_time >= cls.expiration_date)
        if expired_pastes is not None:
            expired_pastes.delete()
            db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def deletion_inbound(self):
        return datetime.utcnow() >= self.expiration_date

    def password_correct(self, password):
        return check_password_hash(self.password, password)

    def __init__(self, owner_name, title, language, password, content, open_edit, expiration):
        self.owner_id = Account.find_by_username(owner_name).id
        self.title = title
        self.language = language
        self.password = None if password == '' else generate_password_hash(password, method='sha256')
        self.content = content
        self.open_edit = (open_edit == 'true')
        self.expiration_date = self.expiration_options.get(expiration)
        self.paste_uuid = str(uuid4())[:8]

    def __repr__(self):
        return '<Paste %r>' % self.title
