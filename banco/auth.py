import functools
from flask import (
    Blueprint,
    g,
    redirect,
    render_template,
    flash,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash
from .db import db_create, db_get, selecionar_agencia
from random import randint
from datetime import datetime as dt

bp = Blueprint("auth", __name__, url_prefix="/")


@bp.route("/cadastro", methods=("GET", "POST"))
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        rg = request.form["rg"]
        rua = request.form["rua"]
        cep = request.form["cep"]
        bairro = request.form["bairro"]
        cidade = request.form["cidade"]
        uf = request.form["uf"]
        numero = request.form["numero"]
        complemento = request.form["complemento"]
        data_nasc = request.form["data-nasc"]
        cpf = request.form["cpf"]
        senha = request.form["senha"]
        senha_repetida = request.form["senha-repetida"]
        tipo = request.form["tipo"]
        genero = request.form["genero"]

        if senha == senha_repetida:
            try:
                novo_usuario = db_create(
                    table="usuario",
                    nome=nome,
                    senha=generate_password_hash(senha),
                    cpf=cpf,
                    data_nasc=data_nasc,
                    rg=rg,
                    cep=cep,
                    rua=rua,
                    bairro=bairro,
                    numero=numero,
                    complemento=complemento,
                    uf=uf,
                    cidade=cidade,
                    genero=genero
               
                    
                )
                contas = list(
                    map(lambda x: x["id_conta"], db_get(table="conta", many=True))
                )
                idconta = randint(11111, 99999)
                while idconta in contas:
                    idconta = randint(11111, 99999)
                agencia = selecionar_agencia()

                nova_conta = db_create(
                    table="conta",
                    id_conta=idconta,
                    saldo=0,
                    usuario=novo_usuario,
                    status="aguardando",
                    tipo=tipo,
                    agencia=agencia,
                    abertura=dt.now(),
                    ultima_cobranca=dt.now(),
                )
            except:
                pass
            else:
                if nova_conta:
                    return redirect(url_for("auth.aguarde", conta=nova_conta))
                else:
                    flash("Erro ao criar conta")
                    return redirect(url_for("auth.login"))
        else:
            flash("As senhas não são compatíveis.")

    return render_template("auth/cadastro.html")


@bp.route("/aguarde")
def aguarde():
    id_conta = request.args.get("conta")
    conta = db_get(table="conta", many=False, id_conta=id_conta)

    return render_template("auth/aguarde.html", conta=conta)


@bp.route("/", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        id_conta = str(request.form["id_conta"])
        id_agencia = request.form["id_agencia"]
        senha = request.form["senha"]
        usuario = None
        error = None

        conta = db_get(many=False, table="conta", id_conta=id_conta)

        if conta:
            id_usuario = conta["usuario"]
            usuario = db_get(many=False, table="usuario", id_usuario=id_usuario)

        if (
            usuario is None
            or conta["agencia"] != int(id_agencia)
            or conta["status"] != "aprovado"
            or conta["tipo"] not in ["corrente", "poupança"]
            or not check_password_hash(usuario["senha"], senha)
        ):
            error = "Conta inexistente"

        if error is None:
            config = db_get(table="config", many=False)
            data = config.get("data")
            session.clear()
            session["id_usuario"] = usuario["id_usuario"]
            session["id_conta"] = conta["id_conta"]
            session["tempo"] = data
            return redirect(url_for("conta.index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@bp.route("/teste")
def teste():
    contas = db_get(table="conta", usuario=400)
    msg = "sapo"
    if not contas:
        msg = "sopa"
    return msg


@bp.before_app_request
def carregar_usuario_logado():
    """Função que é executada antes de requisições
    para determinar o usuário da sessão."""
    id_usuario = session.get("id_usuario")
    id_conta = session.get("id_conta")
    data = session.get("data")

    if id_conta is None or id_usuario is None or data is None:
        g.data = None
        g.usuario = None
        g.conta = None
    else:
        g.usuario = db_get(many=False, table="usuario", id_usuario=id_usuario)
        g.conta = db_get(many=False, table="conta", id_conta=id_conta)
        g.data = data


def requer_login(view):
    """Função que verifica se o usuário está logado.
    Deve ser importada e usada como decorator em rotas que exigem autenticação.
    Caso o usuário não esteja na sessão, retorna para a tela de login.
    """

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.conta is None or g.usuario is None:
            session.clear()
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


def rota_cliente(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if "corrente" not in g.conta["tipo"] and "poupança" not in g.conta["tipo"]:
            return redirect(url_for("admin.pendencias"))

        return view(**kwargs)

    return wrapped_view


def rota_gerente(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if "gerente" not in g.conta["tipo"]:
            return redirect(url_for("conta.index"))

        return view(**kwargs)

    return wrapped_view
