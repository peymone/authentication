from flask import Flask
from . import auth
from . import db
import os


def create_app(production_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        DEBUG=True,
        USERNAME='admin',
        PASSWORD='default',
        SECRET_KEY='development key',   # SECRET_KEY=os.urandom(30)
        DATABASE=os.path.join(app.root_path, 'auth.db')
    )

    if production_config:
        app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)
    app.register_blueprint(auth.blueprint)

    return app
