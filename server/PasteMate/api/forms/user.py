"""
WTForms validation logic for user related forms.
"""
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
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

        if Account.find_by_email(self.email.data):
            self.email.errors.append("Email is already in use.")
            return False

        if Account.find_by_username(self.username.data):
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

        return user


class ChangeEmailForm(Form):
    username = StringField()
    newEmail = StringField(validators=[validators.InputRequired("No new email was given."), validators.Email()])
    currentPassword = StringField(validators=[validators.InputRequired("Current password is required."),
                                              validators.Length(min=4, max=128)])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = Account.find_by_username(self.username.data)

        if not user.password_correct(self.currentPassword.data):
            self.currentPassword.errors.append("Password is incorrect.")
            return False

        if Account.find_by_email(self.newEmail.data):
            self.newEmail.errors.append("Email is already in use.")
            return False

        return user


class ChangePasswordForm(Form):
    username = StringField()
    newPassword = StringField(validators=[validators.InputRequired("New password is required."),
                                          validators.Length(min=4, max=128)])
    currentPassword = StringField(validators=[validators.InputRequired("Current password is required."),
                                              validators.Length(min=4, max=128)])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = Account.find_by_username(self.username.data)

        if not user.password_correct(self.currentPassword.data):
            self.currentPassword.errors.append("Password is incorrect.")
            return False

        return user


class DeleteUserForm(Form):
    username = StringField()
    password = StringField(validators=[validators.InputRequired("Your password is required."), validators.Length(min=4, max=128)])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = Account.find_by_username(self.username.data)

        if not user.password_correct(self.password.data):
            self.password.errors.append("Password is incorrect.")
            return False

        return True


class ResetPasswordFormSend(Form):
    email = StringField(validators=[validators.InputRequired("No email was given."), validators.Email()])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = Account.find_by_email(self.email.data)

        if not user:
            self.email.errors.append("User with specified email was not found.")
            return False

        return user


class ResetPasswordFormReceive(Form):
    token = StringField()
    password = StringField(validators=[validators.InputRequired("No password was given."), validators.Length(min=4, max=128)])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(self.token)
            user = Account.find_by_id(data.get('reset_id'))
            if not user:
                self.token.errors.append("The account this token is for was not found.")
                return False
        except (BadSignature, SignatureExpired):
            self.token.errors.append("This token is invalid or has expired.")
            return False

        return user


