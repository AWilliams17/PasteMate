from os import getcwd
from os.path import exists
from sentry_config.config import SentryConfig, SentrySection, SentryOption
from sentry_config.validators import BoolRequired, StringRequired


class PasteMateConfig(SentryConfig):
    def __init__(self):
        self.ini_path = getcwd() + '/pm.ini'
        super().__init__(self.ini_path)
        if not exists(self.ini_path):
            self.flush_config()
        self.read_config()

    def set_app_config(self, app):  # TODO: I really don't like this being here. Or it looking like this.
        app.config.update({
            'SQLALCHEMY_DATABASE_URI': self.DataBaseOptions.database_uri,
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            'SECRET_KEY': self.SecurityOptions.application_secret_key,
            'CORS_SUPPORTS_CREDENTIALS': True,
            'JWT_SECRET_KEY': self.SecurityOptions.jwt_secret_key,
            'JWT_BLACKLIST_ENABLED': True,
            'JWT_BLACKLIST_TOKEN_CHECKS': ['access', 'refresh'],
            'JWT_COOKIE_CSRF_PROTECT': True,
            'JWT_TOKEN_LOCATION': "cookies",
            'JWT_COOKIE_SECURE': self.SecurityOptions.jwt_cookie_secure,
            'DEBUG': self.ApplicationOptions.debug_mode
        })

    class ApplicationOptions(SentrySection):
        debug_mode = SentryOption(
            default=False,
            criteria=BoolRequired,
            description="Whether or not to run the flask application object in debug mode or not."
        )

    class DataBaseOptions(SentrySection):
        database_uri = SentryOption(
            default="sqlite:///PM.db",
            criteria=StringRequired,
            description="The URI of the database to be used in the application."
        )

    class SecurityOptions(SentrySection):
        jwt_secret_key = SentryOption(
            default="12345",
            criteria=StringRequired,
            description="Secret key used to encrypt JWTs. Defaults to 12345 (Change this)."
        )
        jwt_cookie_secure = SentryOption(
            default=False,
            criteria=BoolRequired,
            description="If enabled, JWTs are only allowed to be sent over HTTPS. Set to True during production."
        )
        application_secret_key = SentryOption(
            default="12345",
            criteria=StringRequired,
            description="The secret key which flask will use to sign cookies. Defaults to 12345 (Change this)"
        )

