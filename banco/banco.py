from flask import Blueprint, g, redirect, render_template, request, url_for

from banco.auth import requer_login

from .db import get_db, db_get

bp = Blueprint("conta", __name__, url_prefix="/conta")


@bp.route("/")
@requer_login
def index():
    cpf = g.usuario["cpf"]

    conta = db_get(many=False, table="conta", cpf=cpf)

    return render_template("principal.html", data=conta)


@requer_login
@bp.route("/saque", methods=("GET", "POST"))
def saque():
    if request.method == "POST":
        v = request.form["valor"]
        cpf = g.usuario["cpf"]
        db = get_db()

        cursor = db.cursor()
        error = None
        if error is None:
            try:
                cursor.execute("SELECT * FROM banco_api.conta WHERE cpf = %s", (cpf))
                conta = cursor.fetchone()
            except:
                error = "Erro ao efetuar o saque."
            else:
                saldo = conta["saldo"]
                id_conta = conta["id_conta"]
                novo_saldo = float(saldo) - float(v)
                cursor.execute(
                    "UPDATE banco_api.conta SET saldo = %s WHERE id_conta = %s",
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
        cpf = g.usuario["cpf"]

        if error is None:
            try:
                cursor.execute(
                    "SELECT saldo FROM banco_api.conta WHERE cpf = %s", (cpf)
                )
                saldo_atual = cursor.fetchone()
                valordeposito = request.form["valordeposito"]
                novo_saldo = float(saldo_atual["saldo"]) + float(valordeposito)
            except:
                error = "Erro ao efetuar o depósito."
                return error
            else:
                if float(valordeposito) <= 0:
                    return "Não é possivel depositar o valor informado."
                else:
                    try:
                        cursor.execute(
                            "UPDATE banco_api.conta SET saldo = %s WHERE cpf = %s",
                            (novo_saldo, cpf),
                        )
                    except:
                        error = "Erro ao efetuar o depósito."
                    else:
                        return redirect(url_for("conta.index"))

    return render_template("deposito.html")
