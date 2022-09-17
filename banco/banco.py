from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from banco.auth import requer_login

from .db import get_db

bp = Blueprint("conta", __name__, url_prefix="/conta")


@bp.route("/")
@requer_login
def index():
    db = get_db()
    cursor = db.cursor()
    cpf = g.usuario["CPF"]
    cursor.execute(
        "SELECT conta_saldo FROM banco_api.conta WHERE CPF = %s",
        (cpf),
    )
    saldo = cursor.fetchone()

    return render_template("principal.html", data=saldo)


@requer_login
@bp.route("/saque", methods=("GET", "POST"))
def saque():
    if request.method == "POST":
        v = request.form["valor"]
        cpf = g.usuario["CPF"]
        db = get_db()

        cursor = db.cursor()
        error = None
        if error is None:
            try:
                cursor.execute("SELECT * FROM banco_api.conta WHERE CPF = %s", (cpf))
                conta = cursor.fetchone()
            except:
                error = "Erro ao efetuar o saque."
            else:
                saldo = conta["conta_saldo"]
                id_conta = conta["id_numero_conta"]
                novo_saldo = float(saldo) - float(v)
                cursor.execute(
                    "UPDATE banco_api.conta SET conta_saldo = %s WHERE id_numero_conta = %s",
                    (novo_saldo, id_conta),
                )
            finally:
                return redirect(url_for("conta.index"))

    return render_template("saque.html")


@bp.route("/deposito", methods=("GET", "POST"))
def deposito():
    if request.method == "POST":
        db = get_db()
        cursor = db.cursor()
        error = None
        cpf = g.usuario["CPF"]

        if error is None:
            try:
                cursor.execute(
                    "SELECT conta_saldo FROM banco_api.conta WHERE CPF = %s", (cpf)
                )
                saldo_atual = cursor.fetchone()
                valordeposito = request.form["valordeposito"]
                novo_saldo = float(saldo_atual["conta_saldo"]) + float(valordeposito)
            except:
                error = "Erro ao efetuar o depósito."
                return error
            else:
                if float(valordeposito) <= 0:
                    return "Não é possivel depositar o valor informado."
                else:
                    try:
                        cursor.execute(
                            "UPDATE banco_api.conta SET conta_saldo = %s WHERE CPF = %s",
                            (novo_saldo, cpf),
                        )
                    except:
                        error = "Erro ao efetuar o depósito."
                    else:
                        return redirect(url_for("conta.index"))

    return render_template("deposito.html")
