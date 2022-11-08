from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    g,
    url_for,
    flash,
    session,
)

from banco.auth import requer_login, rota_gerente

from datetime import datetime

from .db import get_db, db_get, db_update, db_create

from werkzeug.security import check_password_hash, generate_password_hash
from random import randint

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/pendencias", methods=["POST", "GET"])
@requer_login
@rota_gerente
def pendencias():
    if request.method == "POST":
        status = request.form["status"]
        id_transacao = request.form["id_transacao"]
        id_conta = request.form["id_conta"]
        valor = request.form["valor"]

        db = get_db()
        cursor = db.cursor()

        try:
            command = f"""UPDATE transacoes SET status = '{status}', data_fim = '{datetime.now()}' WHERE id_transacao = {id_transacao};"""
            cursor.execute(command)
        except:
            print(command)
            print("Erro ao atualizar transação")
        else:
            if status == "Efetivado":
                conta = db_get(many=False, table="conta", id_conta=id_conta)
                valor_atual = float(conta["saldo"])
                novo_saldo = valor_atual + float(valor)
                command = f"""UPDATE conta SET saldo = {novo_saldo} WHERE id_conta = {id_conta}"""
                print(command)
                cursor.execute(command)

    pendencias = db_get(many=True, table="transacoes", status="aguardando")
    return render_template("adm/pendencias.html", pendencias=pendencias)


@bp.route("/aprovacaoCadastros", methods=["POST", "GET"])
@requer_login
@rota_gerente
def cadastros():
    if request.method == "POST":
        status = request.form["status"]
        id_usuario = request.form["id_usuario"]
        db = get_db()
        cursor = db.cursor()

        try:
            command = (
                f"""UPDATE conta SET status = '{status}' WHERE usuario = {id_usuario}"""
            )
            cursor.execute(command)
        except:
            print(command)
            print("Erro ao atualizar status da conta")
        else:
            conta = db_get(
                table="conta",
                many=False,
                usuario=id_usuario,
                order_by="id_conta",
                order="DESC",
            )
            id_conta = conta["id_conta"]
            msg = f"A conta foi registrada com número {id_conta}"
            flash(msg)

    cadastros = db_get(table="conta", status="Aguardando")
    for conta in cadastros:
        usuario = conta["usuario"]
        usuario = db_get(table="usuario", many=False, id_usuario=usuario)
        conta.update(usuario)

    return render_template("adm/aprovacaoCadastros.html", cadastros=cadastros)


@bp.route("/usuarios", methods=["POST", "GET"])
@requer_login
@rota_gerente
def usuarios():
    contas = None
    ag = g.conta["agencia"]
    if ag:
        contas = db_get(table="conta", agencia=ag)
    else:
        contas = db_get(table="conta")
    dados = []
    for conta in contas:
        usuario = db_get(table="usuario", id_usuario=conta["usuario"], many=False)
        conta.update(usuario)
        conta.pop("senha")
        if conta["tipo"] != "gerente":
            dados.append(conta)

    return render_template("adm/usuarios.html", dados=dados)


@bp.route("/dados", methods=["GET", "POST"])
@requer_login
@rota_gerente
def dados():
    id_usuario = request.args.get("usuario")
    usuario = db_get(many=False, table="usuario", id_usuario=id_usuario)
    data = request.form
    if request.method == "POST":
        for f in data:
            if data[f] != usuario[f]:
                try:
                    db_update(
                        table="usuario",
                        setter={"campo": f, "valor": data[f]},
                        value={"campo": "id_usuario", "valor": id_usuario},
                    )
                except Exception as e:
                    print(e.args[1])
                    flash("Erro ao atualizar cadastro.")
                else:
                    flash("Cadastro atualizado com sucesso!")
                finally:
                    return redirect(url_for("admin.usuarios"))

    for f in ["id_usuario", "senha"]:
        usuario.pop(f)
    return render_template("adm/atualizacaoCadastro.html", usuario=usuario)


@bp.route("/agencias", methods=["GET", "POST"])
@requer_login
@rota_gerente
def agencia():
    db = get_db()
    cursor = db.cursor()
    if request.method == "POST":
        nome = request.form["nome"]

        db_create(table="agencia", nome=nome)

    agencias = db_get(table="agencia", many=True)
    for agencia in agencias:
        gerente = {"nome": None}
        quantidade = db_get(
            count=True, many=False, table="conta", agencia=agencia["id_agencia"]
        )
        command = f"""SELECT * FROM conta WHERE tipo = 'gerente' AND agencia = {agencia['id_agencia']}"""
        cursor.execute(command)
        conta_gerente = cursor.fetchone()
        if conta_gerente:
            gerente = db_get(
                many=False, table="usuario", id_usuario=conta_gerente["usuario"]
            )
        agencia.update(
            {"quantidade": quantidade["COUNT(*)"], "gerente": gerente["nome"]}
        )
    return render_template("adm/agencia.html", agencias=agencias)


@bp.route("/gerentes", methods=["GET", "POST"])
@requer_login
@rota_gerente
def gerente():
    if request.method == "POST":
        nova_agencia = request.form["agencia"]
        gerente_att = request.form["gerente"]
        setter = {"campo": "agencia", "valor": nova_agencia}
        value = {"campo": "id_conta", "valor": gerente_att}
        db_update(table="conta", setter=setter, value=value)

    agencias = db_get(table="agencia")
    gerentes = db_get(table="conta", many=True, tipo="gerente")
    for gerente in gerentes:
        id_usuario = gerente["usuario"]
        usuario = db_get(table="usuario", many=False, id_usuario=id_usuario)
        gerente.update(usuario)
        for agencia in agencias:
            if gerente["agencia"] == agencia["id_agencia"]:
                gerente["agencia_nome"] = agencia["nome"]
                agencias.remove(agencia)

    return render_template("adm/gerente.html", gerentes=gerentes, agencias=agencias)


@bp.route("/cadastrar-gerente", methods=["GET", "POST"])
@requer_login
@rota_gerente
def cadastroGerente():
    if request.method == "POST":
        form = request.form
        nome = form["nome"]
        cpf = form["cpf"]
        senha = form["senha"]
        senha_repetida = form["senha-repetida"]
        if senha == senha_repetida:
            try:
                usuario = db_create(
                    table="usuario",
                    nome=nome,
                    cpf=cpf,
                    senha=generate_password_hash(senha),
                )
            except:
                print("Erro ao cadastrar gerente")
            else:
                contas = list(
                    map(lambda x: x["id_conta"], db_get(table="conta", many=True))
                )
                idconta = randint(11111, 99999)
                while idconta in contas:
                    idconta = randint(11111, 99999)

                db_create(
                    table="conta",
                    id_conta=idconta,
                    status="aprovado",
                    tipo="gerente",
                    usuario=usuario,
                )
            finally:
                return redirect(url_for("admin.gerente"))

    return render_template("adm/cadastroGerentes.html")


@bp.route("/", methods=["POST", "GET"])
def loginadm():
    if request.method == "POST":
        id_conta = str(request.form["id_conta"])
        senha = request.form["senha"]
        usuario = None
        error = None

        conta = db_get(many=False, table="conta", id_conta=id_conta)

        if conta:
            id_usuario = conta["usuario"]
            usuario = db_get(many=False, table="usuario", id_usuario=id_usuario)

        if (
            usuario is None
            or conta["status"] != "aprovado"
            or conta["tipo"] not in ["gerente"]
            or not check_password_hash(usuario["senha"], senha)
            or (conta["agencia"] is None and id_conta != "1")
        ):
            error = "Conta inexistente"

        if error is None:
            session.clear()
            session["id_usuario"] = usuario["id_usuario"]
            session["id_conta"] = conta["id_conta"]
            if id_conta == "1" and conta["saldo"] == None:
                return redirect(url_for("admin.capital_inicial"))
            return redirect(url_for("admin.pendencias"))

        flash(error)

    return render_template("auth/loginadmin.html")


@bp.route("/atualizar-agencia", methods=["GET", "POST"])
@requer_login
@rota_gerente
def atualizarAgencia():
    return render_template("adm/atualizacaoAgencia.html")


@bp.route("/capital-inicial", methods=["POST", "GET"])
@requer_login
@rota_gerente
def capital_inicial():
    if request.method == "POST":
        capital = float(request.form["capital"])
        try:
            db = get_db()
            cursor = db.cursor()
            command = f"""UPDATE conta SET saldo = {capital} WHERE id_conta = 1"""
            cursor.execute(command)
        except:
            print("Erro ao atualizar capital inicial")
        else:
            return redirect(url_for("admin.pendencias"))
    return render_template("adm/capitalinicial.html")
