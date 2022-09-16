from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from banco.auth import requer_login

from .db import get_db

bp = Blueprint("conta", __name__, url_prefix="/conta")


@bp.route("/")
@requer_login
def index():
    return render_template("principal.html")


@bp.route("/sacar", methods=("GET", "POST"))
def saque():
    if request.method == "POST":
        saldo_usuario = 1000
        v = request.form["V"]

        db = get_db()
        cursor = db.cursor()
        error = None
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
        v = request.args.get("V")
        if v < saldo_usuario:
            resp = saldo_usuario - v
        db = get_db()
        cursor = db.cursor()
        error = None
        if error is None:
            try:
                cursor.execute(
                    "UPDATE conta (conta_saldo) VALUES ({{resp}})",
                )
                cursor.commit()
                cursor.close()
            except:
                error = "Erro ao efetuar o saque."
            else:
                return "Seu novo saldo é de {}".format(resp)

    return render_template("saque.html")
@bp.route('/deposito')
def deposito():
    return render_template ('deposito.html')

@bp.route('/depositar')
def deposito():
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
                return f'Seu saldo é de {saldo_usuario}'
    saldo_usuario = 1000
    

    valordeposito = request.args.get('valordeposito')## valor pode ser até centavos 

    if valordeposito == 0:
        return 'Não é possivel depositar o valor informado.'
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
            return 'Seu novo saldo é de {}'.format(saldo)


