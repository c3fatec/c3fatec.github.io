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
            autocommit=True,
        )
    return g.db


def db_create(**params):
    table = params.pop("table")
    keys = ",".join(params.keys())
    values = ""
    for value in params.values():
        values += f"'{value}',"
    values = values.removesuffix(",")

    db = get_db()
    cursor = db.cursor()

    try:
        command = f"INSERT INTO {table} ({keys}) VALUES ({values})"
        cursor.execute(command)
    except Exception as e:
        print("Erro ao ciar instância")
        print(e.args[1])


def db_get(many=True, **params):
    table = params.pop("table")
    key = "".join(params.keys())
    value = "".join(params.values())
    db = get_db()
    cursor = db.cursor()

    try:
        command = f"SELECT * FROM {table} WHERE {key} = '{value}';"
        cursor.execute(command)
    except Exception as e:
        print("Erro ao recuperar os dados")
        print(e.args[1])
    else:
        if many is True:
            response = cursor.fetchall()
        response = cursor.fetchone()

    return response


def db_update(table: str, setter: dict, value: dict):
    db = get_db()
    cursor = db.cursor()
    setter_field = setter["campo"]
    setter_val = setter["valor"]
    value_field = value["campo"]
    value_val = value["valor"]

    if isinstance(setter_val, str):
        setter_val = "'" + setter_val + "'"

    if isinstance(value_val, str):
        value_val = "'" + value_val + "'"

    try:
        command = f"UPDATE {table} SET {setter_field} = {setter_val} WHERE {value_field} = {value_val};"
        cursor.execute(command)
    except Exception as e:
        print("Erro ao atualizar tabela")
        print(e.args[1])


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
