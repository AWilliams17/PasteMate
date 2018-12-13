"""
Paste specific API Resources + some helper functions
"""
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from PasteMate.api.forms.paste import SubmitPasteForm
from PasteMate.models.account import Account
from PasteMate.models.paste import Paste


class PastePermissionValidator:  # Doing this with WTForms seems to be ridiculous, so this will do.
    def __init__(self, paste, username, data=None):  # I still don't like this.
        self.paste = paste
        self.user = Account.find_by_username(username)
        self.data = data

    def validate(self, include_edit_perms=False, include_delete_perms=False):
        if not self.paste:
            return {'errors': 'Paste with specified UUID not found.'}, 404

        user_owns_paste = (self.user.id == self.paste.owner_id)
        paste_requires_password = self.paste.password is not None
        request_password = None if not self.data or 'password' not in self.data else self.data['password']

        if include_edit_perms and not user_owns_paste and not self.paste.open_edit:
            return {'errors': 'You do not own this paste and open edit is not enabled for it.'}, 401

        if include_delete_perms and not user_owns_paste:
            return {'errors': 'You can not delete pastes you do not own.'}, 401

        if paste_requires_password and not user_owns_paste:
            if request_password is None:
                return {'errors': 'Password is required.'}, 401

            elif not self.paste.password_correct(request_password):
                return {'errors': 'Password is incorrect.'}, 401

        return None


class SubmitPaste(Resource):
    @jwt_required
    def post(self):
        data = request.get_json(force=True)
        identity = get_jwt_identity()
        current_user = Account.find_by_username(identity)
        form = SubmitPasteForm.from_json(data)

        if not form.validate():
            return {'errors': form.errors}, 400

        data['owner_name'] = current_user.username

        paste = Paste(**data)
        paste.save_to_db()
        return {'paste_uuid': paste.paste_uuid}, 200


class GetPaste(Resource):
    @jwt_required
    def get(self, paste_uuid):
        identity = get_jwt_identity()
        paste = Paste.find_by_uuid(paste_uuid)
        validators = PastePermissionValidator(paste, identity)
        error = validators.validate()
        if error is not None:
            return error

        return {'paste': paste.paste_dict()}, 200

    @jwt_required
    def post(self, paste_uuid):
        identity = get_jwt_identity()
        paste = Paste.find_by_uuid(paste_uuid)
        data = request.get_json(force=True)
        validators = PastePermissionValidator(paste, identity, data)
        error = validators.validate()
        if error is not None:
            return error

        return {'paste': paste.paste_dict()}, 200


class UpdatePaste(Resource):
    @jwt_required
    def post(self, paste_uuid):
        identity = get_jwt_identity()
        paste = Paste.find_by_uuid(paste_uuid)
        data = request.get_json(force=True)
        validators = PastePermissionValidator(paste, identity, data)

        error = validators.validate(include_edit_perms=True)
        form = SubmitPasteForm.from_json(data)

        if error is not None:
            return error

        if not form.validate():
            return {'errors': form.errors}, 400

        data.pop('password')  # Don't update paste passwords.
        data['change_owner_fields'] = False if not validators.paste.owner_id == validators.user.id else True

        paste.update_paste(**data)
        return {'paste_uuid': paste_uuid}, 200


class DeletePaste(Resource):
    @jwt_required
    def get(self, paste_uuid):
        identity = get_jwt_identity()
        paste = Paste.find_by_uuid(paste_uuid)
        validators = PastePermissionValidator(paste, identity)
        error = validators.validate(include_delete_perms=True)
        if error is not None:
            return error
        paste.delete()
        return {'result': 'Paste deleted.'}, 204


class ListPastes(Resource):
    @jwt_required
    def get(self, page):
        def strf_date(date): return date.strftime("%Y-%m-%d %H:%M:%S") if date is not None else None
        identity = get_jwt_identity()
        current_user = Account.find_by_username(identity)
        paste_pagination = current_user.pastes.paginate(int(page), 10, False)
        pastes = []
        for paste in paste_pagination.items:
            pastes.append({
                'uuid': paste.paste_uuid,
                'title': paste.title,
                'language': paste.language,
                'submission_date': strf_date(paste.submission_date),
                'expiration_date': strf_date(paste.expiration_date),
                'edit_date': strf_date(paste.edit_date),
                'open_edit': paste.open_edit,
                'password_protected': paste.password is not None
            })
        return {'pastes': {
            'current_page': paste_pagination.page,
            'last_page': paste_pagination.pages,
            'next_page_url': ('/api/paste/list/%i' % paste_pagination.next_num) if paste_pagination.has_next else None,
            'prev_page_url': ('/api/paste/list/%i' % paste_pagination.prev_num) if paste_pagination.has_prev else None,
            'data': pastes
        }}
