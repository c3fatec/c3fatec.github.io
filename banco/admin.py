from flask import Blueprint, g, redirect, render_template, request, url_for, flash

from banco.auth import requer_login, rota_gerente

from datetime import datetime

from .db import db_create, get_db, db_get

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/pendencias", methods=["POST", "GET"])
@requer_login
@rota_gerente
def pendencias():
    if request.method == "POST":
        status = request.form["status"]
        id_transacao = request.form["id_transacao"]
        id_conta = request.form["id_conta"]
        valor = request.form["valor"]

        db = get_db()
        cursor = db.cursor()

        try:
            command = f"""UPDATE transacoes SET status = '{status}', data_fim = '{datetime.now()}' WHERE id_transacao = {id_transacao};"""
            cursor.execute(command)
        except:
            print(command)
            print("Erro ao atualizar transação")
        else:
            if status == "Efetivado":
                conta = db_get(many=False, table="conta", id_conta=id_conta)
                valor_atual = float(conta["saldo"])
                novo_saldo = valor_atual + float(valor)
                command = f"""UPDATE conta SET saldo = {novo_saldo} WHERE id_conta = {id_conta}"""
                print(command)
                cursor.execute(command)

    pendencias = db_get(many=True, table="transacoes", status="aguardando")
    return render_template("pendencias.html", pendencias=pendencias)


@bp.route("/cadastros", methods=["POST", "GET"])
@requer_login
@rota_gerente
def cadastros():
    if request.method == "POST":
        status = request.form["status"]
        cpf = request.form["cpf"]
        db = get_db()
        cursor = db.cursor()

        try:
            command = f"""UPDATE conta SET status = '{status}' WHERE cpf = {cpf}"""
            cursor.execute(command)
        except:
            print(command)
            print("Erro ao atualizar status da conta")
        else:
            conta = db_get(
                table="conta", many=False, cpf=cpf, order_by="id_conta", order="DESC"
            )
            id_conta = conta["id_conta"]
            msg = f"A conta foi registrada com número {id_conta}"
            flash(msg)

    cadastros = db_get(table="conta", status="Aguardando")
    for conta in cadastros:
        cpf = conta["cpf"]
        usuario = db_get(table="usuario", many=False, cpf=cpf)
        conta.update(usuario)

    return render_template("cadastros.html", cadastros=cadastros)
