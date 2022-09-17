import click
from flask import current_app, g
import pymysql


def get_db():
    """Função para estabelecer conexão com o banco de dados."""

    if "db" not in g:
        g.db = pymysql.connect(
            host="localhost",
            user=current_app.config["DB_USUARIO"],
            database="banco_api",
            password=current_app.config["DB_SENHA"],
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Função que cria o banco de dados."""

    db = pymysql.connect(
        host="localhost",
        user=current_app.config["DB_USUARIO"],
        database="",
        password=current_app.config["DB_SENHA"],
        cursorclass=pymysql.cursors.DictCursor,
    )
    cursor = db.cursor()

    with current_app.open_resource("schema.sql") as f:
        for comando in f.read().decode("utf8").split(";"):
            if len(comando):
                cursor.execute(comando + ";")
        db.commit()
    db.close()


@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("Base de dados gerada.")


@click.command("drop-db")
def drop_db_command():
    """Função que apaga o banco de dados."""

    db = pymysql.connect(
        host="localhost",
        user=current_app.config["DB_USUARIO"],
        database="",
        password=current_app.config["DB_SENHA"],
        cursorclass=pymysql.cursors.DictCursor,
    )
    cursor = db.cursor()

    cursor.execute("DROP DATABASE IF EXISTS banco_api")
    db.close()
    click.echo("Base de dados apagada.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(drop_db_command)
