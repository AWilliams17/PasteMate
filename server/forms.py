from wtforms import Form, validators
from wtforms.fields import StringField
from models import Account, Paste

class RegistrationForm(Form):
    username = StringField(validators=[validators.InputRequired("No username was given."), validators.Length(min=4, max=25)])
    email = StringField(validators=[validators.InputRequired("No email was given."), validators.Email()])
    password = StringField(validators=[validators.InputRequired("No password was given."), validators.Length(min=4, max=25)])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        username_in_use = Account.query.filter_by(username=self.username.data).first() is not None
        email_in_use = Account.query.filter_by(email=self.email.data).first() is not None

        if username_in_use:
            self.username.errors.append("Username is already in use.")
            return False

        if email_in_use:
            self.email.errors.append("Email is already in use.")
            return False

        return True
