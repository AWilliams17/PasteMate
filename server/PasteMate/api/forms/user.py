"""
wtforms validation logic for user related forms.
"""
from wtforms import Form, validators
from wtforms.fields import StringField
from PasteMate.models.account import Account


class RegistrationForm(Form):
    username = StringField(validators=[validators.InputRequired("No username was given."), validators.Length(min=4, max=12)])
    email = StringField(validators=[validators.InputRequired("No email was given."), validators.Email()])
    password = StringField(validators=[validators.InputRequired("No password was given."), validators.Length(min=4, max=128)])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        email_in_use = Account.find_by_email(self.email.data) is not None
        username_in_use = Account.find_by_username(self.username.data) is not None

        if email_in_use:
            self.email.errors.append("Email is already in use.")
            return False
        if username_in_use:
            self.username.errors.append("Username is already in use.")
            return False

        return True


class LoginForm(Form):
    username = StringField(validators=[validators.InputRequired("No username was given."), validators.Length(min=4, max=12)])
    password = StringField(validators=[validators.InputRequired("No password was given."), validators.Length(min=4, max=128)])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = Account.find_by_username(self.username.data)

        if not user:
            self.username.errors.append("Username not found.")
            return False

        if not user.password_correct(self.password.data):
            self.password.errors.append("Password is incorrect.")
            return False

        return True
