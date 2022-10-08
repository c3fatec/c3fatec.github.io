import json
import re
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

    return render_template("principal.html", comprovantes=comprovantes)


@bp.route("/saque", methods=("GET", "POST"))
@requer_login
@rota_cliente
def saque():
    id = request.args.get("id") or None
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
                status="Efetivado",
                valor=float(v),
                data_inicio=datetime.now(),
                data_fim=datetime.now(),
                tipo="saque",
            )
            saque = db_get(
                table="transacoes",
                many=False,
                id_conta=id_conta,
                order_by="id_transacao",
                order="DESC",
            )
            flash("Saque realizado com sucesso!", "text-success")
            id = saque["id_transacao"]
            return redirect(url_for("conta.saque", id=id))

    return render_template("saque.html", id=id)


@bp.route("/deposito", methods=("GET", "POST"))
@requer_login
@rota_cliente
def deposito():
    id = request.args.get("id") or None
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
                tipo="depósito",
            )
        except:
            print("Erro ao efetuar o depósito.")
        else:
            deposito = db_get(
                table="transacoes",
                many=False,
                id_conta=id_conta,
                order_by="id_transacao",
                order="DESC",
            )
            flash(
                "Depósito realizado com sucesso, aguarde a confirmação!", "text-success"
            )
            id = deposito["id_transacao"]
            return redirect(url_for("conta.deposito", id=id))

    return render_template("deposito.html", id=id)


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

    return render_template("comprovantes.html", comprovantes=comprovantes)


@bp.route("/impressao")
@requer_login
@rota_cliente
def impressao():
    id_transacao = request.args.get("id_transacao")
    comprovante = db_get(table="transacoes", many=False, id_transacao=id_transacao)
    conta = db_get(table="conta", many=False, id_conta=comprovante["id_conta"])
    usuario = db_get(table="usuario", many=False, cpf=conta["cpf"])
    data = {"nome": usuario["nome"], "cpf": usuario["cpf"]}
    comprovante.update(data)
    return render_template("impressao.html", comprovante=comprovante)
