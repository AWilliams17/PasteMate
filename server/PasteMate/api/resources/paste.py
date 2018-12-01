"""
Paste specific API Resources + some helper functions
"""
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from PasteMate.api.forms.paste import SubmitPasteForm
from PasteMate.models.account import Account
from PasteMate.models.paste import Paste


def paste_request_validate(paste, request_data=None):
    """Check if the paste is found, and if the paste is password protected. If the paste is password protected,
    attempt to verify if the passed password is the correct one."""
    if paste is None:
        return {'error': 'Paste with requested UUID was not found.'}, 404

    if paste.password is not None:
        if request_data is None or 'password' not in request_data:
            return {'error': 'password is required.'}, 401

        password = request_data['password']

        if not paste.password_correct(password):
            return {'error': 'password is incorrect.'}, 401

    return None


def validate_paste_edit_permissions(paste, jwt_identity, request_data=None):
    """Verify the user has permission to edit a paste."""
    current_user_id = Account.find_by_username(jwt_identity).id
    validation_errors = paste_request_validate(paste, request_data)
    user_owns_paste = (current_user_id == paste.owner_id)

    if validation_errors is not None:
        return validation_errors

    if not user_owns_paste and not paste.open_edit:
        return {'error': 'You are not the owner of this paste, and open edit is not enabled for it.'}, 401

    return None


class SubmitPaste(Resource):
    @jwt_required
    def post(self):
        data = request.get_json(force=True)
        form = SubmitPasteForm.from_json(data)
        if not form.validate():
            return {'errors': form.errors}, 401
        identity = get_jwt_identity()
        data['owner_id'] = Account.find_by_username(identity).id
        this_paste = Paste(**data)
        this_paste.save_to_db()
        return {'paste_uuid': this_paste.paste_uuid}, 200


class ViewPaste(Resource):
    def get(self, paste_uuid):
        paste = Paste.find_by_uuid(paste_uuid)
        validation_errors = paste_request_validate(paste)
        if validation_errors is not None:
            return validation_errors
        return {'paste': paste.paste_dict()}, 200

    def post(self, paste_uuid):
        print("Validation request post is coming")
        data = request.get_json(force=True)
        paste = Paste.find_by_uuid(paste_uuid)
        validation_errors = paste_request_validate(paste, data)
        if validation_errors is not None:
            return validation_errors
        return {'paste': paste.paste_dict()}, 200


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


class EditPasteGet(Resource):
    """For validating requests to get paste information for editing purposes."""
    @classmethod
    def paste_edit_get(cls, paste, jwt_identity, request_data=None):
        validation_errors = validate_paste_edit_permissions(paste, jwt_identity, request_data)
        if validation_errors is not None:
            return validation_errors

        paste_information = paste.paste_dict()

        for key in ['deletion_inbound', 'expiration_date']:
            paste_information.pop(key)

        paste_information['expiration'] = 0

        return {'paste': paste_information}, 200

    @jwt_required
    def get(self, paste_uuid):
        paste = Paste.find_by_uuid(paste_uuid)
        identity = get_jwt_identity()

        return self.paste_edit_get(paste, identity)

    @jwt_required
    def post(self, paste_uuid):
        paste = Paste.find_by_uuid(paste_uuid)
        identity = get_jwt_identity()
        data = request.get_json(force=True)

        return self.paste_edit_get(paste, identity, data)


class EditPastePost(Resource):
    """For validating requests to update pastes"""
    @jwt_required
    def post(self, paste_uuid):
        paste = Paste.find_by_uuid(paste_uuid)
        identity = get_jwt_identity()
        data = request.get_json(force=True)
        form = SubmitPasteForm.from_json(data)

        if not form.validate():
            return {'errors': form.errors}, 401

        validation_errors = validate_paste_edit_permissions(paste, identity, data)
        if validation_errors is not None:
            return validation_errors

        # TODO: I really don't like hitting the DB twice to get the user ID.
        current_user_id = Account.find_by_username(identity).id
        if paste.owner_id != current_user_id and paste.open_edit:
            # Restrict changes to the password, expiration date, and open edit settings if they are not
            # the paste owner.
            data['password'] = None
            data['open_edit'] = None
            data['expiration'] = None

        paste.update_paste(**data)
        return {'paste_uuid': paste.paste_uuid}, 200
