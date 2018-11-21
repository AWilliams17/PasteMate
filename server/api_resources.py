from flask import after_this_request
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                                jwt_refresh_token_required, get_jwt_identity, get_raw_jwt,
                                set_access_cookies, set_refresh_cookies, unset_jwt_cookies)
from forms import RegistrationForm, LoginForm
from models import Account, Paste, RevokedToken
from datetime import timedelta


parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('email')


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
        data = parser.parse_args()
        form = RegistrationForm.from_json(data)
        if not form.validate():
            return {'errors': form.errors}, 400
        print(data)
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
        data = parser.parse_args()
        form = LoginForm.from_json(data)
        if not form.validate():
            return {'success': False, 'errors': form.errors}, 401
        user = Account.find_by_email(data.get('email'))

        @after_this_request
        def set_jwt_cookies(response):
            user_tokens = create_tokens(user)
            set_cookies(user_tokens, response)
            return response

        return {'success': True, 'errors': None}, 200


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
