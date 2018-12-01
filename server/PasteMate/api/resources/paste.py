"""
Paste specific API Resources + some helper functions
"""
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from PasteMate.api.forms.paste import SubmitPasteForm
from PasteMate.models.account import Account
from PasteMate.models.paste import Paste


def validate_password(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper


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
        if paste is None:
            return {'error': 'Paste with requested UUID was not found.'}, 404
        if paste.password is not None:
            return {'error': 'password is required'}, 401
        return {'paste': paste.paste_dict()}, 200

    def post(self, paste_uuid):
        data = request.get_json(force=True)
        if 'password' in data:
            paste = Paste.find_by_uuid(paste_uuid)
            if paste.password_correct(data['password']):
                return {'paste': paste.paste_dict()}, 200
            return {'error': 'password is incorrect.'}, 401
        return {'error': 'Password required.'}, 401


class EditPaste(Resource):
    @jwt_required
    def get(self, paste_uuid):
        """
        Verify that the paste exists, the user has proper permission to edit the paste, and strip out owner-only
        settings if the editor is not the owner of the paste.
        :param paste_uuid: The UUID of the paste to be edited.
        :return: Status code 404 if the paste was not found, 401 if permissions are not met, and 200 if successful,
        along with appropriate JSON response messages for each of these codes.s
        """
        paste = Paste.find_by_uuid(paste_uuid)
        if paste is None:
            return {'error': 'Paste not found'}, 404
        identity = get_jwt_identity()
        current_user_id = Account.find_by_username(identity).id
        if paste.owner_id != current_user_id and not paste.open_edit:
            return {'error': 'You are not the owner of this paste, and open edit is not enabled for it.'}, 401
        paste_information = paste.paste_dict()
        # Strip out unneeded information and set expiration to 0 for client
        for key in ['deletion_inbound', 'expiration_date']:
            paste_information.pop(key)
        paste_information['expiration'] = 0
        return {'paste': paste_information}, 200

    @jwt_required
    def post(self, paste_uuid):  # Just in case someone tries to get dirty with post requests, verify things here too.
        """
        Same validation regarding permissions is repeated here, with the addition of verifying the submitted
        password
        :param paste_uuid:
        :return:
        """
        paste = Paste.find_by_uuid(paste_uuid)
        if paste is None:
            return {'error': 'Paste not found'}, 404
        data = request.get_json(force=True)
        form = SubmitPasteForm.from_json(data)
        if not form.validate():
            return {'errors': form.errors}, 401
        identity = get_jwt_identity()
        current_user_id = Account.find_by_username(identity).id
        if paste.owner_id != current_user_id and not paste.open_edit:
            return {'error': 'You are not the owner of this paste, and open edit is not enabled for it.'}, 401
        if paste.owner_id != current_user_id and paste.open_edit:
            # Restrict changes to the password, expiration date, and open edit settings if they are not
            # the paste owner.
            data['password'] = None
            data['open_edit'] = None
            data['expiration'] = None
        paste.update_paste(**data)
        return {'paste_uuid': paste.paste_uuid}, 200


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