import os

from flask import Blueprint, render_template, redirect, url_for, flash
from flask import session, request, current_app
from werkzeug.utils import secure_filename


from src.web.helpers.auth import token_required, decode_token
from src.core import auth

perfil_blueprint = Blueprint("perfil", __name__, url_prefix="/perfil")


@perfil_blueprint.get("/")
@token_required
def perfil():
    userToken = decode_token(session["user"])
    if userToken is None:
        return redirect(url_for("auth.logout"))
    user = auth.find_user_by_mail(userToken["user"]).items[0]
    return render_template(
        "user/perfil.html", user=user, editDescription=False, editImg=False
    )


@perfil_blueprint.route("/description", methods=("GET", "POST"))
@token_required
def edit_description():
    userToken = decode_token(session["user"])
    if userToken is None:
        return redirect(url_for("auth.logout"))
    user = auth.find_user_by_mail(userToken["user"]).items[0]
    if request.method == "POST":
        params = request.form
        if params["texDes"]:
            user = auth.edit_description_user(user, params["texDes"].strip())
            flash("Descripción actualizada", "success")
            return render_template(
                "user/perfil.html", user=user, editDescription=False, editImg=False
            )
        else:
            flash("No se envió ninguna descripción", "error")
    return render_template(
        "user/perfil.html", user=user, editDescription=True, editImg=False
    )


ALLOWED_EXTENSIONS = set([".png", ".jpg", ".jpeg"])


@perfil_blueprint.route("/photo/change", methods=("GET", "POST"))
@token_required
def change_photo():
    userToken = decode_token(session["user"])
    if userToken is None:
        return redirect(url_for("auth.logout"))
    user = auth.find_user_by_mail(userToken["user"]).items[0]
    if request.method == "POST":
        file = request.files["archivo"]
        filename = secure_filename(file.filename)  # Nombre original del archivo

        # capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
        extension = os.path.splitext(filename)[1]

        # verifico el tipo de archivo
        if not extension in ALLOWED_EXTENSIONS:
            flash("Tipo de archivo no valido.", "error")
            return redirect(url_for("perfil.perfil"))

        newNameFile = auth.save_photo_user(extension, file, user.email)

        if newNameFile is None:
            flash("Fallo al guardar la foto.", "error")
            return redirect(url_for("perfil.perfil"))

        session["photo"] = newNameFile

        flash("Foto actualizada.", "success")
        return redirect(url_for("perfil.perfil"))
    return render_template(
        "user/perfil.html", user=user, editDescription=False, editImg=True
    )
