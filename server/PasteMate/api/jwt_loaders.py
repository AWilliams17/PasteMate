from PasteMate.db.models import RevokedToken
from flask import jsonify
from flask_jwt_extended import JWTManager

jwt_manager = JWTManager()


@jwt_manager.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedToken.is_jti_blacklisted(jti)


@jwt_manager.expired_token_loader
def expired_token_callback():
    return jsonify({'error': 'token_expired'}), 401


@jwt_manager.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'error': 'invalid_token'}), 401


@jwt_manager.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'error': 'authorization_required'}), 401


@jwt_manager.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({'error': 'fresh_token_required'}), 401


@jwt_manager.revoked_token_loader
def revoked_token_callback():
    return jsonify({'error': 'token_revoked'}), 401
