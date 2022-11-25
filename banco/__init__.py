from flask import Flask
import os
import secrets
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


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

    from . import admin

    # importando rotas de administrador
    app.register_blueprint(admin.bp)

    from . import db

    # registrando comandos de banco de dados
    db.init_app(app)

    # criar filtros

    def dinheiro(txt):
        x = f"{txt:,.2f}"
        txt = str(x)
        a = txt.replace(",", "/")
        b = a.replace(".", ",")
        c = b.replace("/", ".")
        return c

    def primeironome(nome):
        x = nome.split()
        return x[0].capitalize()

    def datetime(data, format="%d/%m/%Y %H:%M:%S"):
        return data.strftime(format)

    def date(data, format="%d/%m/%Y"):
        return data.strftime(format)

    app.add_template_filter(date)
    app.add_template_filter(dinheiro)
    app.add_template_filter(datetime)
    app.add_template_filter(primeironome)

    def aplicar_taxas():
        with app.app_context():
            db.aplicar_taxas()

    def aumentar_data():
        with app.app_context():
            db.aumentar_data()

    trigger = CronTrigger(
        year="*", month="*", day="*", hour="08", minute="27", second="0")

    schedule = BackgroundScheduler(daemon=True)
    schedule.add_job(aplicar_taxas, trigger=trigger)
    schedule.add_job(aumentar_data, trigger=trigger)
    schedule.start()

    return app
