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
from .db import db_create, db_get
from random import randint

bp = Blueprint("auth", __name__, url_prefix="/")


@bp.route("/cadastro", methods=("GET", "POST"))
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        senha = request.form["senha"]
        senha_repetida = request.form["senha-repetida"]
        cpf = request.form["cpf"]

        if senha == senha_repetida:
            try:
                db_create(
                    table="usuario",
                    nome=nome,
                    senha=generate_password_hash(senha),
                    cpf=cpf,
                    tipo="cliente",
                )
            except:
                pass
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
                    saldo=0,
                    cpf=cpf,
                    status="aguardando",
                )
                return redirect(url_for("auth.aguarde"))
        else:
            flash("As senhas não são compatíveis.")

    return render_template("auth/cadastro.html")


@bp.route("/aguarde")
def aguarde():
    return render_template("auth/aguarde.html")


@bp.route("/", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        id_conta = str(request.form["id_conta"])
        senha = request.form["senha"]
        usuario = None
        error = None

        conta = db_get(many=False, table="conta", id_conta=id_conta)

        if conta:
            cpf = conta["cpf"]
            usuario = db_get(many=False, table="usuario", cpf=cpf)

        if usuario is None:
            error = "Conta inexistente"
        elif conta["status"] != "aprovado":
            error = "Conta inexistente"
        elif not check_password_hash(usuario["senha"], senha):
            error = "Conta inexistente"

        if error is None:
            session.clear()
            session["id_usuario"] = usuario["id_usuario"]
            session["id_conta"] = conta["id_conta"]
            if "cliente" in usuario["tipo"]:
                return redirect(url_for("conta.index"))
            else:
                return redirect(url_for("admin.pendencias"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@bp.route("/teste")
def teste():
    contas = list(map(lambda x: x["id_conta"], db_get(table="conta", many=True)))

    idconta = randint(1, 9)
    numbers = [2, 3, 4]
    while idconta in numbers:
        print(idconta)
        idconta = randint(1, 9)
    return [contas, idconta]


@bp.before_app_request
def carregar_usuario_logado():
    """Função que é executada antes de requisições
    para determinar o usuário da sessão."""
    id_usuario = session.get("id_usuario")
    id_conta = session.get("id_conta")

    if id_conta is None or id_usuario is None:
        g.usuario = None
        g.conta = None
    else:
        g.usuario = db_get(many=False, table="usuario", id_usuario=id_usuario)
        g.conta = db_get(many=False, table="conta", id_conta=id_conta)


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
        if "cliente" not in g.usuario["tipo"]:
            return redirect(url_for("admin.pendencias"))

        return view(**kwargs)

    return wrapped_view


def rota_gerente(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if "gerente" not in g.usuario["tipo"]:
            return redirect(url_for("conta.index"))

        return view(**kwargs)

    return wrapped_view
