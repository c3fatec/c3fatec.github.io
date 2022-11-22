import click
from flask import current_app, g
import pymysql
from datetime import datetime as dt
from datetime import timedelta as td
from dateutil.relativedelta import relativedelta

from werkzeug.security import generate_password_hash


def selecionar_agencia(user=None, agencia=None):
    tem_gerente = list(filter(lambda a: a["gerente"], db_get(table="agencia")))
    agencias = list(map(lambda a: a["id_agencia"], tem_gerente))
    if agencia:
        try:
            agencias.remove(agencia)
        except:
            pass
    # if user:
    #     contas = db_get(table="conta", usuario=user)
    #     conta_gerente = next(filter(lambda c: c["tipo"] == "gerente", contas), None)
    #     if (
    #         conta_gerente
    #         and conta_gerente["agencia"]
    #         and conta_gerente["agencia"] in agencias
    #     ):
    #         agencias.remove(conta_gerente["agencia"])
    agencias = list(
        map(
            lambda a: {
                "id": a,
                "count": db_get(count=True, many=False, table="conta", agencia=a)[
                    "COUNT(*)"
                ],
            },
            agencias,
        )
    )
    ag = {}
    if agencias:
        menor = min(list(map(lambda a: a["count"], agencias)))
        ag = next(a for a in agencias if a["count"] == menor)

    return ag.get("id") or "Não há agências disponíveis"


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
        print("Erro ao criar instância")
        print(e.args[1])
    else:
        return db.insert_id()


def db_get(
    count=False,
    many=True,
    limit=None,
    order_by=None,
    order=None,
    date_filter=None,
    **params,
):
    table = params.pop("table")
    key = "".join(params.keys())
    value = ",".join(str(v) for v in params.values())
    db = get_db()
    cursor = db.cursor()
    response = None

    try:
        command = f"SELECT * FROM {table}"
        if count:
            command = f"SELECT COUNT(*) FROM {table}"
        if key and value:
            command += f" WHERE {key} = '{value}'"
        if date_filter:
            command += (
                f" AND data_inicio BETWEEN '{date_filter[0]}' AND '{date_filter[1]}'"
            )
        if order_by:
            command += f" ORDER BY {order_by}"
            if order:
                command += f" {order}"
        if limit:
            command += f" LIMIT {limit}"
        cursor.execute(command)
    except Exception as e:
        print("Erro ao recuperar os dados")
        print(e.args[1])
    else:
        if many is True:
            response = cursor.fetchall()
        else:
            response = cursor.fetchone()
    if response is None:
        print(command)
        print("Erro ao recuperar os dados")
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


def db_delete(table: str, **params):
    key = "".join(params.keys())
    value = ",".join(str(v) for v in params.values())
    db = get_db()
    cursor = db.cursor()
    command = f"""DELETE FROM {table} WHERE {key} = {value}"""
    cursor.execute(command)


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

    # gerente geral
    db_create(
        table="usuario",
        nome="Gabriel Oliveira",
        senha=generate_password_hash("gerente"),
        cpf="52504467876",
    )
    db_create(
        table="conta",
        id_conta=1,
        usuario=1,
        status="aprovado",
        tipo="gerente",
        abertura=dt.now(),
    )

    # agencias
    db_create(table="agencia", nome="Morumbi")
    db_create(table="agencia", nome="Cidade Jardim")
    db_create(table="agencia", nome="Vista Verde")

    # gerentes
    daniel = db_create(
        table="usuario",
        nome="Daniel",
        senha=generate_password_hash("daniel"),
        cpf="11122233344",
    )
    jackles = db_create(
        table="usuario",
        nome="Jackles",
        senha=generate_password_hash("jackles"),
        cpf="22233344455",
    )
    ivan = db_create(
        table="usuario",
        nome="Ivan",
        senha=generate_password_hash("ivan"),
        cpf="33344455566",
    )
    paulista = db_create(
        table="usuario",
        nome="Paulista",
        senha=generate_password_hash("paulista"),
        cpf="44455566677",
    )

    db_create(
        table="conta",
        id_conta=99999,
        usuario=daniel,
        status="aprovado",
        tipo="gerente",
        agencia=1,
        abertura=dt.now(),
    )
    db_create(
        table="conta",
        id_conta=88888,
        usuario=jackles,
        status="aprovado",
        tipo="gerente",
        agencia=2,
        abertura=dt.now(),
    )
    db_create(
        table="conta",
        id_conta=77777,
        usuario=ivan,
        status="aprovado",
        tipo="gerente",
        abertura=dt.now(),
    )
    db_create(
        table="conta",
        id_conta=66666,
        usuario=paulista,
        status="aprovado",
        tipo="gerente",
        abertura=dt.now(),
    )
    cliente_1 = db_create(
        table="usuario",
        nome="Cliente 1",
        senha=generate_password_hash("cliente"),
        cpf="12332112332",
    )
    cliente_2 = db_create(
        table="usuario",
        nome="Cliente 2",
        senha=generate_password_hash("cliente"),
        cpf="12332112333",
    )
    db_create(
        saldo=100,
        table="conta",
        id_conta=10000,
        usuario=cliente_1,
        status="aprovado",
        tipo="poupança",
        agencia=1,
        abertura=dt.now(),
        ultima_cobranca=dt.now(),
    )
    db_create(
        saldo=-100,
        table="conta",
        id_conta=20000,
        usuario=cliente_2,
        status="aprovado",
        tipo="corrente",
        agencia=2,
        abertura=dt.now(),
        ultima_cobranca=dt.now(),
    )
    db_create(table="config", data=dt.now())

    db_execute("UPDATE agencia SET gerente = 99999 WHERE id_agencia = 1")
    db_execute("UPDATE agencia SET gerente = 88888 WHERE id_agencia = 2")
    db.close()


def db_execute(*arg: str):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(arg[0])


def aumentar_data():
    config = db_get(table="config", many=False)
    data = config.get("data")
    data += relativedelta(days=+1)
    db_execute(f"UPDATE config SET data = '{data}'")
    print(f"Data alterada para {data}")


def aplicar_taxas():
    config = db_get(table="config", many=False)
    momento = config["data"]

    poupança = db_get(table="conta", tipo="poupança")

    for conta in poupança:
        ultima = conta["ultima_cobranca"]

        years = momento.year - ultima.year
        tempo = momento.month - ultima.month
        dias = momento.day - ultima.day

        if years:
            tempo += years * 12
        if dias < 0:
            tempo -= 1

        if tempo and tempo > 0:
            taxa = config["taxa_rendimento"]
            banco = db_get(table="conta", many=False, id_conta=1)
            saldo_banco = banco["saldo"]
            saldo = conta["saldo"]
            id_conta = conta["id_conta"]

            for _ in range(tempo):
                aumento = round(saldo * taxa / 100, 2)
                saldo_banco -= aumento
                saldo += aumento
                ultima += relativedelta(months=+1)

            command = (
                f"""UPDATE conta SET saldo = {saldo} WHERE id_conta = {id_conta}"""
            )
            db_execute(command)
            command = f"""UPDATE conta SET ultima_cobranca = '{ultima}' WHERE id_conta = {id_conta}"""
            db_execute(command)
            command = f"""UPDATE conta SET saldo = {saldo_banco} WHERE id_conta = 1"""
            db_execute(command)

    corrente = db_get(table="conta", tipo="corrente")

    for conta in list(filter(lambda c: c.get("saldo") < 0, corrente)):
        ultima = conta["ultima_cobranca"]

        years = momento.year - ultima.year
        tempo = momento.month - ultima.month
        dias = momento.day - ultima.day

        if years:
            tempo += years * 12
        if dias < 0:
            tempo -= 1

        if tempo and tempo > 0:
            taxa = config["taxa_juros"]
            saldo = conta["saldo"]
            id_conta = conta["id_conta"]

            for _ in range(tempo):
                juros = round(saldo * taxa / 100, 2)
                saldo += juros
                ultima += relativedelta(months=+1)

            command = (
                f"""UPDATE conta SET saldo = {saldo} WHERE id_conta = {id_conta}"""
            )
            db_execute(command)
            command = f"""UPDATE conta SET ultima_cobranca = '{ultima}' WHERE id_conta = {id_conta}"""
            db_execute(command)

    print("Taxas aplicadas")


@click.command("change-time")
@click.option("--time", default=None, type=str)
def change_system_time(time):
    try:
        new_time = None
        if time:
            new_time = dt.strptime(time, "%Y-%m-%d")
        else:
            new_time = dt.now()
    except:
        print("Inserir data no formato (yyyy-mm-dd)")
        print(time)
    else:
        config = db_get(many=False, table="config")
        tempo_atual = config["data"]

        years = new_time.year - tempo_atual.year
        tempo = new_time.month - tempo_atual.month
        dias = new_time.day - tempo_atual.day

        if years:
            tempo += years * 12
        if dias < 0:
            tempo -= 1

        if tempo < 0:
            contas = list(
                filter(lambda c: c["tipo"] != "gerente", db_get(table="conta"))
            )
            for conta in contas:
                ultima = conta["ultima_cobranca"]
                ultima += relativedelta(months=+tempo)
                id_conta = conta["id_conta"]
                command = f"""UPDATE conta SET ultima_cobranca = '{ultima}' WHERE id_conta = {id_conta}"""
                db_execute(command)
        db_execute(f"UPDATE config SET data = '{new_time}'")
        config = db_get(many=False, table="config")
        print(config["data"])


@click.command("tax")
def tax():
    aplicar_taxas()


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
    app.cli.add_command(change_system_time)
    app.cli.add_command(tax)
