from logging import warning
from flask import Blueprint, g, redirect, render_template, request, url_for, flash

from banco.auth import requer_login

from .db import db_create, get_db, db_get

from datetime import datetime

bp = Blueprint("conta", __name__, url_prefix="/conta")


@bp.route("/")
@requer_login
def index():

    conta = g.conta
    id_conta = conta["id_conta"]
    comprovantes = db_get(many=True, limit=3, table="transacoes", id_conta=id_conta)

    return render_template("principal.html", data=conta, comprovantes=comprovantes)


@bp.route("/saque", methods=("GET", "POST"))
@requer_login
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
            return redirect(url_for("conta.saque"))

    conta = g.conta
    return render_template("saque.html", data=conta)


@bp.route("/deposito", methods=("GET", "POST"))
@requer_login
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
            flash(
                "Depósito realizado com sucesso, aguarde a aprovação!", "text-success"
            )
            return redirect(url_for("conta.deposito"))

    conta = g.conta
    return render_template("deposito.html", data=conta)


@bp.route("/comprovantes")
@requer_login
def comprovantes():
    conta = g.conta
    id_conta = conta["id_conta"]
    comprovantes = db_get(many=True, table="transacoes", id_conta=id_conta)
    return render_template("comprovantes.html", data=conta, comprovantes=comprovantes)
