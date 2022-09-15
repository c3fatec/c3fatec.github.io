from flask import Flask
import os
import secrets


def create_app():
    app = Flask(__name__)

    secret_key = secrets.token_hex(16)
    app.config["SECRET_KEY"] = secret_key

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import auth

    app.register_blueprint(auth.bp)

    from . import banco

    app.register_blueprint(banco.bp)

    from . import db

    db.init_app(app)

    return app
