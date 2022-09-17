import functools
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db

bp = Blueprint("auth", __name__, url_prefix="/")


@bp.route("/cadastro", methods=("GET", "POST"))
def cadastro():
    if request.method == "POST":
        # return request.form
        nome = request.form["nome"]
        senha = request.form["senha"]
        cpf = request.form["cpf"]
        db = get_db()
        cursor = db.cursor()
        error = None

        if not nome:
            error = "Informe seu nome"
        elif not senha:
            error = "Informe sua senha"
        elif not cpf:
            error = "Informe seu cpf"

        if error is None:
            try:
                cursor.execute(
                    "INSERT INTO banco_api.usuario (CPF, nome_usuario, senha_usuario) VALUES (%s, %s, %s)",
                    (cpf, nome, generate_password_hash(senha)),
                )
            except:
                error = "Erro ao efetuar o cadastro."
            else:
                cursor.execute(
                    "INSERT INTO banco_api.conta (conta_saldo, CPF) values (%s, %s)",
                    (2000, cpf),
                )
            finally:
                return "Cadastro efetuado"

        print(error)

    return render_template("auth/cadastro.html")


@bp.route("/", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        numero_conta = str(request.form["numero_conta"])
        senha = request.form["senha_usuario"]
        db = get_db()
        cursor = db.cursor()
        error = None
        cursor.execute(
            "SELECT CPF FROM conta WHERE id_numero_conta = %s", (numero_conta)
        )
        cpf = cursor.fetchone()
        cursor.execute("SELECT * FROM usuario WHERE CPF = %s", (cpf["CPF"]))
        usuario = cursor.fetchone()
        if usuario is None:
            error = "Esta conta não existe"

        elif not check_password_hash(usuario["senha_usuario"], senha):
            error = "Senha incorreta"

        if error is None:
            session.clear()
            session["id_usuario"] = usuario["id_usuario"]
            return redirect(url_for("conta.deposito"))

        flash(error)

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
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM  usuario WHERE id_usuario = %s", (id_usuario,))
        g.usuario = cursor.fetchone()


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
