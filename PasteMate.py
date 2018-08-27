from flask import Flask, render_template
from flask_session import Session
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)
app.debug = True


@app.route('/')
def index():
    return render_template("base.html")


if __name__ == '__main__':
    session = Session()
    session.init_app(app)
    app.run()
