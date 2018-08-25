from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("base.html")


if __name__ == '__main__':
    app.run()
