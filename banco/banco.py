from flask import Blueprint, g, redirect, render_template, request, url_for, flash

from banco.auth import requer_login, rota_cliente

from .db import db_create, get_db, db_get

from datetime import datetime

bp = Blueprint("conta", __name__, url_prefix="/conta")


@bp.route("/")
@requer_login
@rota_cliente
def index():

    conta = g.conta
    id_conta = conta["id_conta"]
    comprovantes = db_get(
        many=True,
        order_by="id_transacao",
        order="DESC",
        limit=5,
        table="transacoes",
        id_conta=id_conta,
    )

    return render_template("cliente/home.html", comprovantes=comprovantes)


@bp.route("/saque", methods=("GET", "POST"))
@requer_login
@rota_cliente
def saque():
    id = request.args.get("id") or None
    if request.method == "POST":
        v = request.form["valor"]
        db = get_db()
        cursor = db.cursor()

        try:
            saldo = g.conta["saldo"]
            id_conta = g.conta["id_conta"]
            novo_saldo = float(saldo) - float(v)
            banco = db_get(table="conta", many=False, id_conta=1)
            capital_banco = banco["saldo"]
            novo_capital = float(capital_banco) - float(v)
            if novo_capital >= 0:
                cursor.execute(
                    "UPDATE conta SET saldo = %s WHERE id_conta = 1", novo_capital
                )
                cursor.execute(
                    "UPDATE banco_api.conta SET saldo = %s WHERE id_conta = %s",
                    (novo_saldo, id_conta),
                )
            else:
                raise Exception(f"{capital_banco}, {novo_capital}")

        except Exception as e:
            flash("Impossível efetuar o saque")
            print(e)
            return redirect(url_for("conta.saque", id=None))

        else:
            db_create(
                table="transacoes",
                id_conta=id_conta,
                status="Efetivado",
                valor=float(v),
                data_inicio=datetime.now(),
                data_fim=datetime.now(),
                tipo="saque",
            )
            saque = db_get(
                table="transacoes",
                many=False,
                id_conta=id_conta,
                order_by="id_transacao",
                order="DESC",
            )
            flash("Saque realizado com sucesso!")
            id = saque["id_transacao"]
            return redirect(url_for("conta.saque", id=id))

    return render_template("cliente/saque.html", id=id)


@bp.route("/deposito", methods=("GET", "POST"))
@requer_login
@rota_cliente
def deposito():
    id = request.args.get("id") or None
    if request.method == "POST":
        v = request.form["valor"]

        try:
            id_conta = g.conta["id_conta"]
            db_create(
                table="transacoes",
                id_conta=id_conta,
                valor=float(v),
                status="Aguardando",
                data_inicio=datetime.now(),
                tipo="depósito",
            )
        except:
            print("Erro ao efetuar o depósito.")
        else:
            deposito = db_get(
                table="transacoes",
                many=False,
                id_conta=id_conta,
                order_by="id_transacao",
                order="DESC",
            )
            flash(
                "Depósito realizado com sucesso, aguarde a confirmação!", "text-success"
            )
            id = deposito["id_transacao"]
            return redirect(url_for("conta.deposito", id=id))

    return render_template("cliente/deposito.html", id=id)


@bp.route("/extrato", methods=["GET", "POST"])
@requer_login
@rota_cliente
def extrato():
    conta = g.conta
    id_conta = conta["id_conta"]
    date_filter = None

    if request.method == "POST":
        data_inicio = " ".join(request.form["data_inicio"].split("T")) + ":00"
        data_fim = " ".join(request.form["data_fim"].split("T")) + ":00"
        date_filter = [data_inicio, data_fim]

    db = get_db()
    cursor = db.cursor()
    command = f"""SELECT * FROM transacoes WHERE  id_conta = {id_conta} OR destino = {id_conta}"""
    if date_filter:
        command += f" AND data_inicio BETWEEN '{date_filter[0]}' AND '{date_filter[1]}'"
    command += " ORDER BY data_inicio DESC"
    cursor.execute(command)
    comprovantes = cursor.fetchall()

    return render_template("cliente/extrato.html", comprovantes=comprovantes)


@bp.route("/impressao")
@requer_login
@rota_cliente
def impressao():
    id_transacao = request.args.get("id_transacao")
    comprovante = db_get(table="transacoes", many=False, id_transacao=id_transacao)
    conta = db_get(table="conta", many=False, id_conta=comprovante["id_conta"])
    usuario = db_get(table="usuario", many=False, id_usuario=conta["usuario"])
    data = {"nome": usuario["nome"], "cpf": usuario["cpf"]}
    comprovante.update(data)
    if comprovante["destino"]:
        destino_conta = db_get(
            table="conta", many=False, id_conta=comprovante["destino"]
        )
        destino = db_get(
            table="usuario", id_usuario=destino_conta["usuario"], many=False
        )
        data = {"nome_destino": destino["nome"]}
        comprovante.update(data)
    return render_template("cliente/impressao.html", comprovante=comprovante)


@bp.route("/transferencia", methods=["POST", "GET"])
@requer_login
@rota_cliente
def transferir():
    db = get_db()
    cursor = db.cursor()
    id = None
    if request.method == "POST":
        valor = request.form["valor"]
        conta = request.form["conta"]
        agencia = request.form["agencia"]
        try:
            command = f"""SELECT * FROM conta WHERE id_conta = {int(conta)} AND agencia = {int(agencia)}"""
            cursor.execute(command)
            recipiente = cursor.fetchone()
            if not recipiente or int(conta) == g.conta["id_conta"]:
                raise Exception("Esta conta não existe")
        except:
            flash("Esta conta não existe")
        else:
            try:
                saldo = g.conta["saldo"]
                id_conta = g.conta["id_conta"]
                novo_saldo = float(saldo) - float(valor)
                if novo_saldo < 0 and g.conta["tipo"] == "poupança":
                    flash("Impossível realizar transação")
                    return redirect(url_for("conta.transferir"))
                cursor.execute(
                    "UPDATE banco_api.conta SET saldo = %s WHERE id_conta = %s",
                    (novo_saldo, id_conta),
                )
            except:
                pass
            else:
                saldo_r = recipiente["saldo"]
                novo_saldo_r = float(saldo_r) + float(valor)
                cursor.execute(
                    "UPDATE conta SET saldo = %s WHERE id_conta = %s",
                    (novo_saldo_r, int(conta)),
                )
                id = db_create(
                    table="transacoes",
                    id_conta=id_conta,
                    status="Efetivado",
                    data_inicio=datetime.now(),
                    tipo="Transferência",
                    valor=float(valor),
                    destino=int(conta),
                )
                flash("Transferência realizada com sucesso!")

    return render_template("cliente/transferencia.html", id=id)
