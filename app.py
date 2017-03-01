from flask import Flask
from models import *


APP_NAME = 'client-ms'
app = Flask(APP_NAME)
app.config['SECRET_KEY'] = 'c88ecc3d91285be04a60c0b68fbceedf'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/anvesh/projects/client-ms/client-ms.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./client-ms.db'

CURRENT_USER_SESSION_KEY = "currentUser"


def init_db():
    db.init_app(app)
    db.create_all(app=app)


if __name__ == '__main__':
    from routes import *
    init_db()
    app.run(debug=True)
