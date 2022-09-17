from crypt import methods
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from banco.auth import requer_login

from .db import get_db

bp = Blueprint("conta", __name__, url_prefix="/conta")


@bp.route("/")
@requer_login
def index():
    return render_template("principal.html")


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
                cursor.execute(
                    "SELECT conta_saldo FROM banco_api.conta WHERE id_numero_conta = %s",
                    id_conta,
                )
                saldo = cursor.fetchone()
                return f"Saque efetuado, seu saldo agora é de {saldo['conta_saldo']}"

    return render_template("saque.html")


@bp.route("/deposito", methods=("GET", "POST"))
def deposito():
    if request.method == "POST":
        db = get_db()
        cursor = db.cursor()
        error = None
        saldo_usuario = 1000

        if error is None:
            try:
                cursor.execute(
                    "UPDATE conta (conta_saldo) VALUES ({{saldo_usuario}})",
                )
                cursor.commit()
                cursor.close()
            except:
                error = "Erro ao efetuar o cadastro."
            else:
                return f"Seu saldo é de {saldo_usuario}"
        saldo_usuario = 1000

        valordeposito = request.args.get(
            "valordeposito"
        )  ## valor pode ser até centavos

        if valordeposito == 0:
            return "Não é possivel depositar o valor informado."
        else:
            saldo = saldo_usuario + valordeposito

        db = get_db()
        cursor = db.cursor()
        error = None
        if error is None:
            try:
                cursor.execute(
                    "UPDATE conta (conta_saldo) VALUES ({{saldo}})",
                )
                cursor.commit()
                cursor.close()
            except:
                error = "Erro ao efetuar o deposito."
            else:
                return "Seu novo saldo é de {}".format(saldo)

    return render_template("deposito.html")
