from flask import Blueprint
from flask import render_template, request
from flask import flash, redirect, url_for
from flask import session

from src.core import auth
from src.web.helpers.auth import is_authenticated, generate_token


auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_blueprint.get("/")
def login():
    """HTML del formulario del login"""
    return render_template("auth/login.html")


@auth_blueprint.post("/authenticate")
def authenticate():
    """Verifica que el usuario este registrado"""
    params = request.form

    user = auth.find_user_by_mail_pass(params["email"], params["password"])

    if not user:
        flash("Email o contraseña incorrecta.", "error")
        return redirect(url_for("auth.login"))

    if not auth.email_tiene_permisos(user.email, "start_session_web_admin"):
        flash("Usuario no autorizado.", "error")
        return redirect(url_for("auth.login"))

    if not user.active:
        flash("Usuario bloqueado.", "error")
        return redirect(url_for("auth.login"))

    session["user"] = generate_token(user.email)
    session["name"] = user.first_name + " " + user.last_name
    session["photo"] = user.photo
    flash("La sesión se inició correctamente.", "success")

    return redirect(url_for("home"))


@auth_blueprint.get("/logout")
def logout():
    """Cierra la sesion y redirige al loggin"""
    if is_authenticated(session):
        del session["user"]
        del session["name"]
        del session["photo"]
        session.clear()
        flash("La sesión se cerró correctamente.", "success")

    return redirect(url_for("auth.login"))
