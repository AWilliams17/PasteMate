from flask import Flask, render_template, session
from flask_session import Session
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)
app.debug = True


@app.context_processor
def inject_user():
    return dict(_session=dict(session))


@app.route('/')
def index():
    return render_template("base.html")


if __name__ == '__main__':
    _session = Session()
    _session.init_app(app)
    app.run()
