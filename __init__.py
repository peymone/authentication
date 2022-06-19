from flask import Flask
from . import auth
from . import mail
from . import db
import os


def create_app(production_config=None):
    app = Flask(__name__)

    app.config.from_mapping(
        DEBUG=True,
        USERNAME='admin',
        PASSWORD='default',
        SECRET_KEY='development key',   # SECRET_KEY=os.urandom(30)
        DATABASE=os.path.join(app.root_path, 'auth.db'),

        MAIL_SERVER='smtp.mail.ru',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USE_TLS=False,
        MAIL_DEFAULT_SENDER='Gid305@bk.ru',
        MAIL_USERNAME='Gid305@bk.ru',           # Try to change
        MAIL_PASSWORD='hi5Kt85VRG1yxtwyJE3Y'
    )

    if production_config:
        app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)
    mail.init_app(app)
    app.register_blueprint(auth.blueprint)

    return app
