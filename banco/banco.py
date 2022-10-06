from flask import Blueprint, g, redirect, render_template, request, url_for

from banco.auth import requer_login

from .db import db_create, get_db

from datetime import datetime

bp = Blueprint("conta", __name__, url_prefix="/conta")


@bp.route("/")
@requer_login
def index():

    conta = g.conta

    return render_template("principal.html", data=conta)


@requer_login
@bp.route("/saque", methods=("GET", "POST"))
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
        except:
            print("Erro ao efetuar o saque.")
        else:
            db_create(
                table="transacoes",
                id_conta=id_conta,
                status="completa",
                valor=float(v),
                data_inicio=datetime.now(),
                data_fim=datetime.now(),
                tipo="saque",
            )
        finally:
            return redirect(url_for("conta.index"))

    return render_template("saque.html")


@bp.route("/deposito", methods=("GET", "POST"))
def deposito():
    if request.method == "POST":
        v = request.form["valor"]

        try:
            id_conta = g.conta["id_conta"]
            db_create(
                table="transacoes",
                id_conta=id_conta,
                valor=float(v),
                status="aguardando",
                data_inicio=datetime.now(),
                tipo="deposito",
            )
        except:
            print("Erro ao efetuar o depósito.")
        finally:
            return redirect(url_for("conta.index"))

    return render_template("deposito.html")
