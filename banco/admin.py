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

from .db import (
    db_delete,
    get_db,
    db_get,
    db_update,
    db_create,
    selecionar_agencia,
    db_execute,
)

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
                cursor.execute(command)
                banco = db_get(many=False, table="conta", id_conta=1)
                capital = banco["saldo"]
                novo_capital = float(capital) + float(valor)
                command = (
                    f"""UPDATE conta SET saldo = {novo_capital} WHERE id_conta = 1"""
                )
                cursor.execute(command)
                flash("Transação aprovada")
                return redirect(url_for("admin.pendencias"))

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
            agencia = conta["agencia"]
            id_conta = conta["id_conta"]
            msg = f"A conta foi registrada com número {id_conta} na agência {agencia}."
            flash(msg)

    cadastros = db_get(table="conta", status="Aguardando")
    for conta in cadastros:
        if g.conta["agencia"] and conta["agencia"] != g.conta["agencia"]:
            cadastros.remove(conta)
        else:
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
        command = f"""SELECT COUNT(*) FROM conta WHERE agencia = {agencia['id_agencia']} AND tipo != 'gerente'"""
        cursor.execute(command)
        quantidade = cursor.fetchone()
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
def cadastrar_gerente():
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
                    abertura=datetime.now(),
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


@bp.route("/logoutadmin")
def logoutadmin():
    session.clear()
    return redirect(url_for("admin.loginadm"))


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


@bp.route("/atualizar-gerente", methods=["POST", "GET"])
@requer_login
@rota_gerente
def atualizar_gerente():
    id_gerente = request.args["gerente"]
    conta = db_get(table="conta", many=False, id_conta=id_gerente)
    gerente = db_get(table="usuario", many=False, id_usuario=conta["usuario"])

    if request.method == "POST":
        for f in request.form:
            if request.form[f] != gerente[f]:
                setter = {"campo": f, "valor": request.form[f]}
                value = {"campo": "id_usuario", "valor": gerente["id_usuario"]}
                db_update(table="usuario", setter=setter, value=value)

        flash("Dados atualizados.")
        return redirect(url_for("admin.gerente"))

    return render_template("adm/atualizargerente.html", gerente=gerente)


@bp.route("excluir-ag")
@requer_login
@rota_gerente
def excluir_agencia():
    id_agencia = int(request.args["agencia"])
    contas = db_get(table="conta", agencia=id_agencia)
    msg = None
    if contas:
        for conta in contas:
            nova_agencia = selecionar_agencia(agencia=id_agencia)
            if type(nova_agencia) is int:
                if conta["tipo"] == "gerente":
                    db = get_db()
                    cursor = db.cursor()
                    command = f"""UPDATE conta SET agencia = NULL WHERE id_conta = {conta['id_conta']}"""
                    cursor.execute(command)
                else:
                    setter = {"campo": "agencia", "valor": nova_agencia}
                    value = {"campo": "id_conta", "valor": conta["id_conta"]}
                    db_update(table="conta", setter=setter, value=value)
            else:
                msg = nova_agencia
    if msg is None:
        db_delete(table="agencia", id_agencia=id_agencia)
        msg = "Agência excluída."
    flash(msg)
    return redirect(url_for("admin.agencia"))


@bp.route("atualizar-agencia", methods=["POST", "GET"])
@requer_login
@rota_gerente
def atualizar_agencia():
    db = get_db()
    cursor = db.cursor()
    id_agencia = int(request.args["agencia"])
    agencia = db_get(table="agencia", many=False, id_agencia=id_agencia)
    command = (
        f"""SELECT * FROM conta WHERE tipo = 'gerente' AND agencia = {id_agencia}"""
    )
    cursor.execute(command)
    gerente_atual = cursor.fetchone()
    if gerente_atual:
        usr = db_get(table="usuario", many=False, id_usuario=gerente_atual["usuario"])
        data = {
            "gerente": usr["id_usuario"],
            "gerente_nome": usr["nome"],
            "gerente_conta": gerente_atual["id_conta"],
        }
        agencia.update(data)

    if request.method == "POST":
        gerente = int(request.form["gerente"])
        nome = request.form["nome"]
        if nome != agencia["nome"]:
            db_update(
                table="agencia",
                setter={"campo": "nome", "valor": nome},
                value={"campo": "id_agencia", "valor": id_agencia},
            )
        if gerente and gerente != agencia.get("gerente"):
            command = f"""SELECT * FROM conta WHERE tipo = 'gerente' AND usuario = {gerente}"""
            cursor.execute(command)
            gerente = cursor.fetchone()
            db_update(
                table="conta",
                setter={"campo": "agencia", "valor": id_agencia},
                value={"campo": "id_conta", "valor": gerente["id_conta"]},
            )
            db_update(
                table="agencia",
                setter={"campo": "gerente", "valor": gerente["id_conta"]},
                value={"campo": "id_agencia", "valor": id_agencia},
            )
            if agencia.get("gerente_conta"):
                command = f"""UPDATE conta SET agencia = NULL WHERE id_conta = {agencia['gerente_conta']}"""
                cursor.execute(command)
        elif not gerente and agencia.get("gerente_conta"):
            db_update(
                table="conta",
                setter={"campo": "agencia", "valor": None},
                value={"campo": "id_conta", "valor": agencia["gerente_conta"]},
            )
        return redirect(url_for("admin.agencia"))

    command = """SELECT * FROM conta WHERE tipo = 'gerente' AND agencia IS NULL AND id_conta != 1"""
    cursor.execute(command)
    gerentes = cursor.fetchall()
    for gerente in gerentes:
        usr = db_get(table="usuario", many=False, id_usuario=gerente["usuario"])
        gerente["nome"] = usr["nome"]

    return render_template(
        "adm/atualizaragencia.html", agencia=agencia, gerentes=gerentes
    )


@bp.route("/taxas", methods=["GET", "POST"])
@requer_login
@rota_gerente
def taxas():
    config = db_get(table="config", many=False)
    if request.method == "POST":
        if request.form.get("juros") != config.get("taxa_juros"):
            db_execute(f"UPDATE config SET taxa_juros = {request.form.get('juros')}")
        if request.form.get("rendimento") != config.get("taxa_rendimento"):
            db_execute(
                f"UPDATE config SET taxa_rendimento = {request.form.get('rendimento')}"
            )
        return redirect(url_for("admin.taxas"))

    return render_template("adm/taxas.html", config=config)
