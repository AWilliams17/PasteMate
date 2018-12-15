"""
User specific API resources + JWT auxiliary functions
"""
from flask import after_this_request, request
from flask_restful import Resource
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,
                                jwt_refresh_token_required, get_jwt_identity, get_raw_jwt,
                                set_access_cookies, set_refresh_cookies, unset_jwt_cookies)
from PasteMate.api.forms.user import (RegistrationForm, LoginForm, ChangeEmailForm,
                                      ChangePasswordForm, DeleteUserForm,
                                      ResetPasswordFormSend, ResetPasswordFormReceive)
from PasteMate.api.mail import send_reset_token
from PasteMate.models.account import Account
from PasteMate.models.revoked_token import RevokedToken
from datetime import timedelta


def create_tokens(user):
    """
    Creates an access and refresh token using the username as the identity for the token.
    :param user: The user object, the type being the SQLAlchemy Model instance.
    :return: A list containing the access token first, and then the refresh token.
    """
    access_expiration = timedelta(days=7)  # Access Tokens expire after 7 days.
    refresh_expiration = timedelta(days=14)  # Refresh Tokens expire after 14 days.
    access_token = create_access_token(identity=user.username, fresh=True, expires_delta=access_expiration)
    refresh_token = create_refresh_token(identity=user.username, expires_delta=refresh_expiration)
    return [access_token, refresh_token]


def set_cookies(tokens, response):
    """
    Helper function which takes a flask response object and calls JWT's set cookies functions
    on it using the JWT tokens.
    :param tokens: A list containing the access token as the first member, and the refresh token as the second.
    :param response: A flask response object
    """
    set_access_cookies(response, tokens[0])
    set_refresh_cookies(response, tokens[1])


def revoke_access(response):
    """
    Unsets the JWT related cookies in the response, then returns the modified response.
    :param response: The flask response object to set the headers in.
    :return: The modified response.
    """
    jti = get_raw_jwt()
    revoked_token = RevokedToken(jti=jti['jti'])
    revoked_token.save_to_db()
    unset_jwt_cookies(response)
    return response


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

        return {'username': user.username, 'userID': user.id, 'email': user.email}, 201


class LoginUser(Resource):
    def post(self):
        data = request.get_json(force=True)
        form = LoginForm.from_json(data)

        if not form.validate():
            return {'errors': form.errors}, 401

        user = Account.find_by_username(data.get('username'))  # TODO: Polling the database twice.

        @after_this_request
        def set_jwt_cookies(response):
            user_tokens = create_tokens(user)
            set_cookies(user_tokens, response)
            return response

        return {'username': user.username, 'userID': user.id, 'email': user.email}, 200


class UpdateEmail(Resource):
    @jwt_required
    def post(self):
        current_username = get_jwt_identity()
        user = Account.find_by_username(current_username)  # TODO: Polling the database twice.
        data = request.get_json(force=True)
        data['username'] = current_username
        form = ChangeEmailForm.from_json(data)

        if not form.validate():
            return {'errors': form.errors}, 401

        user.update_email(data['newEmail'])

        return {'success': 'Successfully changed account email address to %s' % data['newEmail']}, 201


class UpdatePassword(Resource):
    @jwt_required
    def post(self):
        current_username = get_jwt_identity()
        user = Account.find_by_username(current_username)  # TODO: Polling the database twice.
        data = request.get_json(force=True)
        data['username'] = current_username
        form = ChangePasswordForm.from_json(data)

        if not form.validate():
            return {'errors': form.errors}, 401

        user.update_password(data['newPassword'])

        return {'success': 'Successfully changed account password.'}, 201


class DeleteUser(Resource):
    @jwt_required
    def post(self):
        current_username = get_jwt_identity()
        user = Account.find_by_username(current_username)  # TODO: Polling the database twice.
        data = request.get_json(force=True)
        data['username'] = current_username
        form = DeleteUserForm.from_json(data)

        if not form.validate():
            return {'errors': form.errors}, 401

        @after_this_request
        def deauthenticate(response):
            return revoke_access(response)

        Account.delete(user.id)

        return {'success': 'Account has been deleted.'}, 201


class ResetPasswordSend(Resource):
    """ For sending reset password tokens via email """
    def post(self):
        data = request.get_json(force=True)
        form = ResetPasswordFormSend.from_json(data)

        if not form.validate():
            return {'errors': form.errors}, 401

        user = Account.find_by_email(data['email'])  # TODO: Polling the database twice for LITERALLY the same thing.
        token = user.generate_password_reset_token()
        send_reset_token(token, user.email)

        return {'success': 'Password reset request received. Please wait a while and check your inbox/spam.'}, 200


class ResetPasswordReceive(Resource):
    """ For receiving the reset password tokens, and then using the passed password to reset the account password. """
    def post(self):
        data = request.get_json(force=True)
        form = ResetPasswordFormReceive.from_json(data)
        token_data = form.validate()

        if not token_data:
            return {'errors': form.errors}, 401

        user = Account.find_by_id(token_data.get('reset_id'))  # TODO: Polling the database twice for LITERALLY the same thing, again.
        user.update_password(data['password'])

        return {'success': 'Account with email %s has been successfully updated.' % user.email}, 200


class RevokeAccess(Resource):
    @jwt_required
    def get(self):

        @after_this_request
        def deauthenticate(response):
            return revoke_access(response)

        return {'token_revoked': True}, 200


class RefreshUser(Resource):
    @jwt_refresh_token_required
    def get(self):
        current_username = get_jwt_identity()
        access_token = create_access_token(identity=current_username)
        response = {'token_refreshed': True}

        @after_this_request
        def set_new_cookies():
            set_access_cookies(response, access_token)
            return response

        return response, 200


class CurrentUser(Resource):
    @jwt_required
    def get(self):
        current_username = get_jwt_identity()
        user = Account.find_by_username(current_username)

        if user:
            return {'username': current_username, 'userID': user.id, 'email': user.email}

        return {'errors': 'Account not found.'}, 400
        # Nothing else needed since the loader should do the rest.
