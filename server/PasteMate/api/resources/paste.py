"""
Paste specific API Resources + some helper functions
"""
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from PasteMate.api.forms.paste import SubmitPasteForm, ValidatePastePermissions
from PasteMate.models.account import Account
from PasteMate.models.paste import Paste


def validate_permissions(user, paste, data=None, validate_delete_perms=False, validate_edit_perms=False):
    if not paste or paste.deletion_inbound():  # The reason for checking if a deletion is inbound is if the deletion
        return {"errors": "Paste with specified UUID was not found."}, 404  # job for that paste hasn't run yet.

    permission_data = {
        "user": user,
        "paste": paste,
        "validate_delete": validate_delete_perms,
        "validate_edit": validate_edit_perms,
        "password": None if not data or (len(data) == 0 or 'password' not in data) else data.get('password')
    }

    v = ValidatePastePermissions.from_json(permission_data)

    if not v.validate():
        return {"errors": v.errors}, 401

    return None


class SubmitPaste(Resource):
    @jwt_required
    def post(self):
        data = request.get_json(force=True)
        current_user = Account.find_by_username(get_jwt_identity())
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
        user = Account.find_by_username(get_jwt_identity())
        paste = Paste.find_by_uuid(paste_uuid)

        permissions_errors = validate_permissions(user, paste)
        if permissions_errors:
            return permissions_errors

        return {'paste': paste.paste_dict()}, 200

    @jwt_required
    def post(self, paste_uuid):
        user = Account.find_by_username(get_jwt_identity())
        paste = Paste.find_by_uuid(paste_uuid)
        data = request.get_json(force=True)

        permissions_errors = validate_permissions(user, paste, data)
        if permissions_errors:
            return permissions_errors

        return {'paste': paste.paste_dict()}, 200


class UpdatePaste(Resource):
    @jwt_required
    def post(self, paste_uuid):
        data = request.get_json(force=True)
        user = Account.find_by_username(get_jwt_identity())
        paste = Paste.find_by_uuid(paste_uuid)

        permissions_errors = validate_permissions(user, paste, data, validate_edit_perms=True)
        if permissions_errors:
            return permissions_errors

        submission_validator = SubmitPasteForm.from_json(data)

        if not submission_validator.validate():
            return {'errors': submission_validator.errors}, 400

        data.pop('password')  # Don't update paste passwords.
        data['change_owner_fields'] = False if not (paste.owner_id == user.id) else True
        paste.update_paste(**data)

        return {'paste_uuid': paste_uuid}, 200


class DeletePaste(Resource):
    @jwt_required
    def get(self, paste_uuid):
        user = Account.find_by_username(get_jwt_identity())
        paste = Paste.find_by_uuid(paste_uuid)

        permissions_errors = validate_permissions(user, paste, validate_delete_perms=True)
        if permissions_errors:
            return permissions_errors

        paste.delete()
        return {'result': 'Paste deleted.'}, 204


class ListPastes(Resource):
    @jwt_required
    def get(self, page):
        def strf_date(date): return date.strftime("%Y-%m-%d %H:%M:%S") if date is not None else None
        current_user = Account.find_by_username(get_jwt_identity())
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
