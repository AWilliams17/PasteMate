"""
wtforms validation logic for paste related forms.
"""
from wtforms import Form, validators
from wtforms.fields import StringField, BooleanField, IntegerField
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
