app_config = {  # The security settings are all terrible. But this is never going up anywhere.
    'SQLALCHEMY_DATABASE_URI': "sqlite:///PM.db",
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SECURITY_PASSWORD_SALT': "12345",
    'SECRET_KEY': "12345",
    'CORS_SUPPORTS_CREDENTIALS': True,
    'JWT_SECRET_KEY': "12345",
    'JWT_BLACKLIST_ENABLED': True,
    'JWT_BLACKLIST_TOKEN_CHECKS': ['access', 'refresh'],
    'JWT_COOKIE_CSRF_PROTECT': True,
    'JWT_TOKEN_LOCATION': "cookies",
    'JWT_COOKIE_SECURE': False,
    'DEBUG': True
}