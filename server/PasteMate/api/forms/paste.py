"""
wtforms validation logic for paste related forms.
"""
from wtforms import Form, validators
from wtforms.fields import StringField, BooleanField, IntegerField, Field
from PasteMate.api.hljs_list import language_list


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


class ValidatePastePermissions(Form):
    paste = Field()
    user = Field()
    password = StringField(validators=[validators.Length(max=128)])

    def validate(self):
        Form.validate(self)
        if not self.paste:
            self.paste.errors.append("NotFound")
            return False

        target_paste = self.paste.data
        editor = self.user.data

        paste_is_open_edit = target_paste.open_edit
        editor_owns_paste = (target_paste.owner_id == editor.id)
        paste_requires_password = target_paste.password is not None

        if not editor_owns_paste and not paste_is_open_edit:
            self.paste.errors.append("You are not authorized for this action.")
            return False
        if paste_requires_password and not editor_owns_paste:
            if self.password.data is None:
                self.password.errors.append("A password is required to edit this paste.")
                return False
            if not target_paste.password_correct(self.password.data):
                self.password.errors.append("Password is incorrect.")
                return False

        return True
