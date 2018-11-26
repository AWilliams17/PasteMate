from flask import after_this_request, request, jsonify, json, Response
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                                jwt_refresh_token_required, get_jwt_identity, get_raw_jwt,
                                set_access_cookies, set_refresh_cookies, unset_jwt_cookies)
from forms import RegistrationForm, LoginForm, SubmitPasteForm
from models import Account, Paste, RevokedToken
from datetime import timedelta


def create_tokens(user):
    access_expiration = timedelta(days=7)
    refresh_expiration = timedelta(days=14)
    access_token = create_access_token(identity=user.username, fresh=True, expires_delta=access_expiration)
    refresh_token = create_refresh_token(identity=user.username, expires_delta=refresh_expiration)
    return [access_token, refresh_token]


def set_cookies(tokens, response):
    set_access_cookies(response, tokens[0])
    set_refresh_cookies(response, tokens[1])


class RegisterUser(Resource):
    def post(self):
        data = request.get_json(force=True)
        form = RegistrationForm.from_json(data)
        if not form.validate():
            return {'errors': form.errors}, 400
        user = Account(**data)
        user.save_to_db()

        @after_this_request
        def set_jwt_cookies(response):
            user_tokens = create_tokens(user)
            set_cookies(user_tokens, response)
            return response

        return {'username': user.username, 'userID': user.id}, 201


class LoginUser(Resource):
    def post(self):
        data = request.get_json(force=True)
        form = LoginForm.from_json(data)
        if not form.validate():
            return {'errors': form.errors}, 401
        user = Account.find_by_username(data.get('username'))

        @after_this_request
        def set_jwt_cookies(response):
            user_tokens = create_tokens(user)
            set_cookies(user_tokens, response)
            return response

        return {'username': user.username, 'userID': user.id}, 200


class SubmitPaste(Resource):
    @jwt_required
    def post(self):
        data = request.get_json(force=True)
        print(data)
        form = SubmitPasteForm.from_json(data)
        if not form.validate():
            return {'errors': form.errors}, 401
        identity = get_jwt_identity()
        data['owner_id'] = Account.find_by_username(identity).id
        print(data)
        this_paste = Paste(**data)
        this_paste.save_to_db()
        return {'paste_uuid': this_paste.paste_uuid}, 200


class ViewPaste(Resource):
    def get(self, paste_uuid):
        paste = Paste.find_by_uuid(paste_uuid)
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


class RevokeAccess(Resource):
    @jwt_required
    def get(self):
        @after_this_request
        def revoke_access(response):
            jti = get_raw_jwt()
            revoked_token = RevokedToken(jti=jti['jti'])
            revoked_token.save_to_db()
            unset_jwt_cookies(response)
            return response
        return {'token_revoked': True}, 200


class RefreshUser(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        response = {'token_refreshed': True}
        set_access_cookies(response, access_token)
        return response, 200


class CurrentUser(Resource):
    @jwt_required
    def get(self):
        identity = get_jwt_identity()
        user_id = Account.find_by_username(identity).id
        return {'username': identity, 'userID': user_id}
        # Nothing else needed since the loader should do the rest.
