from flask import Blueprint, g, redirect, render_template, request, url_for

from banco.auth import requer_login

from .db import db_create, get_db, db_get

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
                valor=float(v),
                data=datetime.now(),
                tipo="saque",
            )
        finally:
            return redirect(url_for("conta.index"))

    return render_template("saque.html")


@bp.route("/deposito", methods=("GET", "POST"))
def deposito():
    if request.method == "POST":
        v = request.form["valor"]
        db = get_db()
        cursor = db.cursor()

        try:
            id_conta = g.conta["id_conta"]
            saldo = g.conta["saldo"]
            novo_saldo = float(saldo) + float(v)
            cursor.execute(
                "UPDATE banco_api.conta SET saldo = %s WHERE id_conta = %s",
                (novo_saldo, id_conta),
            )
        except:
            print("Erro ao efetuar o depósito.")
        else:
            db_create(
                table="transacoes",
                id_conta=id_conta,
                valor=float(v),
                data=datetime.now(),
                tipo="deposito",
            )
        finally:
            return redirect(url_for("conta.index"))

    return render_template("deposito.html")
