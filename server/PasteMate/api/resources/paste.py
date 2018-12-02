"""
Paste specific API Resources + some helper functions
"""
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from PasteMate.api.forms.paste import SubmitPasteForm
from PasteMate.models.account import Account
from PasteMate.models.paste import Paste


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
        current_user.set_last_used_paste_password(data['password'])

        paste = Paste(**data)
        paste.save_to_db()
        return {'paste_uuid': paste.paste_uuid}, 200


class ViewPaste(Resource):
    @jwt_required
    def get(self, paste_uuid):
        paste = Paste.find_by_uuid(paste_uuid)
        identity = get_jwt_identity()
        current_user = Account.find_by_username(identity)

        return {'paste': paste.paste_dict()}, 200

    @jwt_required
    def post(self, paste_uuid):
        paste = Paste.find_by_uuid(paste_uuid)
        identity = get_jwt_identity()
        current_user = Account.find_by_username(identity)
        data = request.get_json(force=True)

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
    @jwt_required
    def get(self, paste_uuid):
        paste = Paste.find_by_uuid(paste_uuid)
        identity = get_jwt_identity()


    @jwt_required
    def post(self, paste_uuid):
        paste = Paste.find_by_uuid(paste_uuid)
        identity = get_jwt_identity()
        data = request.get_json(force=True)



class EditPastePost(Resource):
    """For validating requests to update pastes"""
    @jwt_required
    def post(self, paste_uuid):
        paste = Paste.find_by_uuid(paste_uuid)
        identity = get_jwt_identity()
        data = request.get_json(force=True)

        
        paste.update_paste(**data)
        return {'paste_uuid': paste.paste_uuid}, 200
