from flask import Blueprint, g, redirect, render_template, request, url_for

from banco.auth import requer_login

from datetime import datetime

from .db import db_create, get_db, db_get

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/", methods=["POST", "GET"])
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
            if status == "completa":
                conta = db_get(many=False, table="conta", id_conta=id_conta)
                valor_atual = float(conta["saldo"])
                novo_saldo = valor_atual + float(valor)
                command = f"""UPDATE conta SET saldo = {novo_saldo} WHERE id_conta = {id_conta};"""
                cursor.execute(command)

    pendencias = db_get(many=True, table="transacoes", status="aguardando")
    return render_template("pendencias.html", data=pendencias)
