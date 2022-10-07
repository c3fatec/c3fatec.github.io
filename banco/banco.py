from logging import warning
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

    return render_template("principal.html", data=conta, comprovantes=comprovantes)

import webbrowser
@bp.route("/saque", methods=("GET", "POST"))
@requer_login
@rota_cliente
def saque():
    if request.method == "POST":
        v = request.form["valor"]
        db = get_db()
        cursor = db.cursor()

        try:
            saldo = g.conta["saldo"]
            id_conta = g.conta["id_conta"]
            novo_saldo = float(saldo) - float(v)
            cursor.execute(
                "UPDATE banco_api.conta SET saldo = %s WHERE id_conta = %s",
                (novo_saldo, id_conta),
            )
            # webbrowser.open_new_tab("https://google.com/")
        except:
            print("Erro ao efetuar o saque.")
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
        finally:
            return redirect(url_for("conta.saque"))

    conta = g.conta
    return render_template("saque.html", data=conta)


@bp.route("/deposito", methods=("GET", "POST"))
@requer_login
@rota_cliente
def deposito():
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
                tipo="deposito",
            )
        except:
            print("Erro ao efetuar o depósito.")
        finally:
            flash(
                "Depósito realizado com sucesso, aguarde a aprovação!", "text-success"
            )
            return redirect(url_for("conta.deposito"))

    conta = g.conta
    return render_template("deposito.html", data=conta)


@bp.route("/comprovantes", methods=["GET", "POST"])
@requer_login
@rota_cliente
def comprovantes():
    conta = g.conta
    id_conta = conta["id_conta"]
    date_filter = None

    if request.method == "POST":
        data_inicio = " ".join(request.form["data_inicio"].split("T")) + ":00"
        data_fim = " ".join(request.form["data_fim"].split("T")) + ":00"
        date_filter = [data_inicio, data_fim]

    comprovantes = db_get(
        many=True,
        order_by="id_transacao",
        order="DESC",
        table="transacoes",
        id_conta=id_conta,
        date_filter=date_filter,
    )
    return render_template("comprovantes.html", data=conta, comprovantes=comprovantes)

@bp.route("/impressao")
@requer_login
@rota_cliente
def impressao():
    return render_template("impressao.html")
