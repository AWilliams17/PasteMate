from flask import current_app
from flask_mail import Mail, Message
from threading import Thread


class AsyncMailSender:
    def init_app(self, app):
        self.app = app
        self.mail = Mail(app)

    def send(self, msg):
        with self.app.app_context():
            self.mail.send(msg)


async_mail = AsyncMailSender()


def send_reset_token(token, receiver):
    reset_link = "{0}?token={1}".format(current_app.config['API_URL'], token)
    msg = Message(
        recipients=[receiver],
        subject='Reset PasteMate Account Password',
        html="""
        <h3>Hello</h3>
        <p>Your request to reset your password has been received.<p>
        <a href="%s">To finalize the request, press here.</a>
        <p>If you did not request a password reset, ignore this message.</p>
        """ % reset_link  # TODO: Better template for this.
    )
    thr = Thread(target=async_mail.send, args=[msg])
    thr.start()
