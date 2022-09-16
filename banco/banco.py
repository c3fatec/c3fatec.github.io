from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from banco.auth import requer_login

from .db import get_db

bp = Blueprint("conta", __name__, url_prefix="/conta")


@bp.route("/")
@requer_login
def index():
    return render_template("principal.html")  

@bp.route("/saque")
def saque():
    return render_template("saque.html")


@bp.route('/sacar', methods=['GET'])
def sacar(): 
    saldo_usuario = 1000
    v = request.args.get('V')
    
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
                return f'Seu saldo é de {saldo_usuario}'
    saldo_usuario = 1000
    v = request.args.get('V')
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
                return 'Seu novo saldo é de {}'.format(resp)
            


@bp.route('/deposito')
def deposito():
    saldo_usuario = 1000
    return''