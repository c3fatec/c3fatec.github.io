from flask import Flask
import os
import secrets


def create_app():
    """Função responsável por determinar as configurações e rotas
    para criar o app."""

    app = Flask(__name__, instance_relative_config=True)

    secret_key = secrets.token_hex(16)
    app.config["SECRET_KEY"] = secret_key
    app.config["DB_USUARIO"] = "root"
    app.config["DB_SENHA"] = ""
    app.config.from_pyfile("config.py")
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import auth

    # importando rotas de autenticação
    app.register_blueprint(auth.bp)

    from . import banco

    # importando rotas de transação
    app.register_blueprint(banco.bp)

    from . import db

    # registrando comandos de banco de dados
    db.init_app(app)

    return app
