import functools
from flask import (
    Blueprint,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash
from .db import db_create, db_get

bp = Blueprint("auth", __name__, url_prefix="/")


@bp.route("/cadastro", methods=("GET", "POST"))
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        senha = request.form["senha"]
        cpf = request.form["cpf"]

        try:
            db_create(
                table="usuario", nome=nome, senha=generate_password_hash(senha), cpf=cpf
            )
        except:
            pass
        else:
            db_create(table="conta", saldo=0, cpf=cpf)
        finally:
            return redirect(url_for("auth.login"))

    return render_template("auth/cadastro.html")


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
            error = "Esta conta não existe"
        elif not check_password_hash(usuario["senha"], senha):
            error = "Senha incorreta"

        if error is None:
            session.clear()
            session["id_usuario"] = usuario["id_usuario"]
            return redirect(url_for("conta.index"))

        print(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@bp.before_app_request
def carregar_usuario_logado():
    """Função que é executada antes de requisições
    para determinar o usuário da sessão."""
    id_usuario = session.get("id_usuario")

    if id_usuario is None:
        g.usuario = None
    else:
        g.usuario = db_get(many=False, table="usuario", id_usuario=id_usuario)


def requer_login(view):
    """Função que verifica se o usuário está logado.
    Deve ser importada e usada como decorator em rotas que exigem autenticação.
    Caso o usuário não esteja na sessão, retorna para a tela de login.
    """

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.usuario is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
