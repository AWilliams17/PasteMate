"""
JWTManager loader definitions, along with the JWTManager instance
to be initialized with the flask app object.
"""
from flask import jsonify
from flask_jwt_extended import JWTManager
from PasteMate.models.revoked_token import RevokedToken


jwt_manager = JWTManager()


@jwt_manager.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedToken.is_jti_blacklisted(jti)


@jwt_manager.expired_token_loader
def expired_token_callback():
    return jsonify({'token_expired': 'This token has expired.'}), 401


@jwt_manager.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'token_invalid': 'This token is invalid: %s' % error}), 401


@jwt_manager.unauthorized_loader
def unauthorized_token(error):
    return jsonify({'token_unauthorized': 'Token is unauthorized: %s' % error}), 401


@jwt_manager.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({'token_old': 'A fresh token is required.'}), 401


@jwt_manager.revoked_token_loader
def revoked_token_callback():
    return jsonify({'token_revoked': 'This token has been revoked.'}), 401
