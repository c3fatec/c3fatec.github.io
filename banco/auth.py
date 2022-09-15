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
        nome = request.form["nome"]
        senha = request.form["senha"]
        cpf = request.form["cpf"]
        data_nasc = request.form["data_nasc"]
        db = get_db()
        cursor = db.cursor()
        error = None

        if not nome:
            error = "Informe seu nome"
        elif not senha:
            error = "Informe sua senha"
        elif not cpf:
            error = "Informe seu cpf"
        elif not data_nasc:
            error = "Informe sua data de nascimento"

        if error is None:
            try:
                cursor.execute(
                    "INSERT INTO usuario (nome, senha, cpf, data_nasc) VALUES (?, ?)",
                    (nome, generate_password_hash(senha), cpf, data_nasc),
                )
                cursor.commit()
                cursor.close()
            except:
                error = "Erro ao efetuar o cadastro."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/cadastro.html")


@bp.route("/", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        cpf = request.form["cpf"]
        senha = request.form["senha"]
        db = get_db()
        cursor = db.cursor()
        error = None
        cursor.execute("SELECT * FROM usuario WHERE cpf = %s", (cpf))
        usuario = cursor.fetchone()

        if usuario is None:
            error = "CPF incorreto"

        elif not check_password_hash(usuario["senha"], senha):
            error = "Senha incorreta"

        if error is None:
            session.clear()
            session["id_usuario"] = usuario["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.before_app_request
def carregar_usuario_logado():
    id_usuario = session.get("id_usuario")

    if id_usuario is None:
        g.usuario = None
    else:
        g.usuario = (
            get_db()
            .execute("SELECT * FROM  usuario WHERE id = ?", (id_usuario,))
            .fetchone()
        )


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def requer_login(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.usuario is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
