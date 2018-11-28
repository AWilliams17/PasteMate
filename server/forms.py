from wtforms import Form, validators
from wtforms.fields import StringField, BooleanField, IntegerField
from models import Account, Paste
from hljs_list import language_list


class RegistrationForm(Form):
    username = StringField(validators=[validators.InputRequired("No username was given."), validators.Length(min=4, max=12)])
    email = StringField(validators=[validators.InputRequired("No email was given."), validators.Email()])
    password = StringField(validators=[validators.InputRequired("No password was given."), validators.Length(min=4, max=128)])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        email_in_use = Account.find_by_email(self.email.data) is not None
        username_in_use = Account.find_by_email(self.username.data) is not None

        if email_in_use:
            self.email.errors.append("Email is already in use.")
            return False
        elif username_in_use:
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


class SubmitPasteForm(Form):
    title = StringField(validators=[validators.Length(min=1, max=24)])
    content = StringField(validators=[validators.InputRequired("Pastes cannot be empty."), validators.Length(min=1, max=600000)])
    language = StringField(validators=[validators.InputRequired("A language must be selected.")])
    expiration = IntegerField(validators=[validators.AnyOf([*range(0, 8)], "A valid expiration option must be selected.")])
    password = StringField(validators=[validators.Length(max=128)])
    open_edit = BooleanField(validators=[validators.AnyOf([False, True], "You must specify if the paste will have open-edit enabled.")])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        if self.language.data not in language_list:
            self.language.errors.append("Please specify a valid language for the paste.")
            return False

        return True
