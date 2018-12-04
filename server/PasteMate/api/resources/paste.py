"""
Paste specific API Resources + some helper functions
"""
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from PasteMate.api.forms.paste import SubmitPasteForm
from PasteMate.models.account import Account
from PasteMate.models.paste import Paste


class PasteValidators:  # Still way better than what I had down earlier.
    def __init__(self, paste_uuid, username, data=None):
        self.paste = Paste.find_by_uuid(paste_uuid)
        self.user = Account.find_by_username(username)
        self.data = data
        self.errors = {}
        self.user_owns_paste = (self.user.id == self.paste.owner_id)
        self.paste_requires_password = self.paste.password is not None
        self.request_password = None if self.data is None or 'password' not in self.data else self.data['password']

    def validate_exists(self):
        if self.paste is None:
            return {'error': 'Paste with requested UUID was not found.'}, 404
        return None

    def validate_password(self):
        if self.paste_requires_password and not self.user_owns_paste:
            if self.request_password is None:
                return {'errors': 'Password is required.'}, 401
            if not self.paste.password_correct(self.request_password):
                return {'errors': 'Password is incorrect.'}, 401
        return None

    def validate_edit_permissions(self):
        if not self.user_owns_paste and not self.paste.open_edit:
            return {'errors': 'You do not own that paste and open edit is not enabled for it.'}, 401
        return None


class SubmitPaste(Resource):
    @jwt_required
    def post(self):
        data = request.get_json(force=True)
        identity = get_jwt_identity()
        current_user = Account.find_by_username(identity)
        form = SubmitPasteForm.from_json(data)

        if not form.validate():
            return {'errors': form.errors}, 401

        data['owner_name'] = current_user.username

        paste = Paste(**data)
        paste.save_to_db()
        return {'paste_uuid': paste.paste_uuid}, 200


class GetPaste(Resource):
    @jwt_required
    def get(self, paste_uuid):
        identity = get_jwt_identity()
        validators = PasteValidators(paste_uuid, identity)
        exists_error = validators.validate_exists()
        password_errors = validators.validate_password()
        if exists_error is not None:
            return exists_error
        elif password_errors is not None:
            return password_errors
        else:
            return {'paste': validators.paste.paste_dict()}, 200

    @jwt_required
    def post(self, paste_uuid):
        identity = get_jwt_identity()
        data = request.get_json(force=True)
        validators = PasteValidators(paste_uuid, identity, data)
        exists_error = validators.validate_exists()
        password_errors = validators.validate_password()
        if exists_error is not None:
            return exists_error
        elif password_errors is not None:
            return password_errors
        else:
            return {'paste': validators.paste.paste_dict()}, 200


class UpdatePaste(Resource):
    @jwt_required
    def post(self, paste_uuid):
        identity = get_jwt_identity()
        data = request.get_json(force=True)
        validators = PasteValidators(paste_uuid, identity, data)
        exists_error = validators.validate_exists()
        password_errors = validators.validate_password()
        edit_perm_errors = validators.validate_edit_permissions()
        if exists_error is not None:
            return exists_error
        if password_errors is not None:
            return password_errors
        if edit_perm_errors is not None:
            return edit_perm_errors

        data['password'] = None  # Don't update paste passwords.

        if not validators.user_owns_paste:
            data['open_edit'] = None
            data['expiration'] = None

        validators.paste.update_paste(**data)
        return {'paste_uuid': validators.paste.paste_uuid}, 200


class DeletePaste(Resource):
    @jwt_required
    def get(self, paste_uuid):
        paste = Paste.find_by_uuid(paste_uuid)
        identity = get_jwt_identity()
        current_user_id = Account.find_by_username(identity).id
        if paste is None:
            return {'error': 'Paste not found'}, 404
        if paste.owner_id != current_user_id:
            return {'error': 'You can not delete pastes you do not own.'}, 401
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
