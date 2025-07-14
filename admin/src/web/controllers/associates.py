from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from src.core import sports
from src.core import setting
from src.core import associates
from src.core import payments
from src.core import licenses
from src.web.helpers.auth import token_required, user_has_permission, token_required
from werkzeug.utils import secure_filename
import os
import qrcode
from PIL import Image
from random import sample
import shutil

associated_blueprint = Blueprint("associates", __name__, url_prefix="/asociados")


@associated_blueprint.post("/new/<int:current_page>")
@token_required
@user_has_permission("associates_new")
def add_associated(current_page):
    """Recibe datos y crea un nuevo asociado. Luego Redirecciona."""
    params = request.form
    result = associates.verify_new_associated(params)
    if not result["associated"]:
        flash(result["message"], "error")
        return render_template(
            "associates/new_associated.html", return_page=current_page
        )
    flash(result["message"], "success")
    return redirect(url_for("associates.associated_index_page", num=current_page))


@associated_blueprint.get("/<int:num>")
@token_required
@user_has_permission("associates_index")
def associated_index_page(num):
    """Trae asociados paginadas."""
    associated = associates.list_associates_page(
        num, setting.get_setting().cant_elements_page
    )
    return render_template(
        "associates/associates.html",
        associates=associated,
        filterState=[False, "", "", ""],
    )


@associated_blueprint.get("/detalle/<int:associated_id>/<int:current_page>")
@token_required
@user_has_permission("associates_index")
def associated_detail(associated_id, current_page):
    """Muestra la ventana con los datos del asociado"""
    associated = associates.get_associated_by_id(associated_id)
    return render_template(
        "associates/associated_detail.html",
        associated=associated,
        current_page=current_page,
    )


def corroborarEstado(estate):
    if estate == "bloqueado":
        return "No-activo"
    return "Activo"


ALLOWED_EXTENSIONS = set([".png", ".jpg", ".jpeg"])

def stringRandom():
    """Genera un string aleatorio"""
    string_random = "0123456789abcdefghijkmnopqrstuvwxyz_"
    long = 20
    sequence = string_random.upper()
    result_random = sample(sequence, long)
    string_random = "".join(result_random)
    return string_random


def save_photo_associated(extension, file):
    """Crea un nuevo nombre y guarda la foto en la ruta por defecto"""
    # asigno un nombre nuevo random, para evitar coincidencias
    newNameFile = stringRandom() + extension

    # establezco la ruta para guardar y lo guardo
    upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], "images/users", newNameFile)
    file.save(upload_path)
    file.close()

    # actualizo la foto del usuario
    return newNameFile

    
def save_qr_associated(associated_id):
    """Genera codigo qr"""
    cadena = f"https://admin-grupo17.proyecto2022.linti.unlp.edu.ar/asociados/carnet/detalles/{associated_id}/1"
    imagen = qrcode.make(cadena)

    nombre_imagen = stringRandom() + ".png"
    archivo_imagen = open(nombre_imagen, 'wb')
    imagen.save(archivo_imagen)
    archivo_imagen.close()
    
    origen = os.path.join("./", nombre_imagen)
    destino = os.path.join(current_app.config["UPLOAD_FOLDER"], "images/qr")
    
    shutil.move(origen,destino)

    return nombre_imagen

@associated_blueprint.post("/carnet/generar/<associated_id>/<int:current_page>")
@token_required
@user_has_permission("carnet_new")
def create_credential(associated_id, current_page):
    """Crea un carnet para un asociado con una imagen, qr y sus datos personales en la BD."""
    file = request.files["archivo"]
    if file:
        filename = secure_filename(file.filename)
        extension = os.path.splitext(filename)[1]
        if not extension in ALLOWED_EXTENSIONS:
            flash("Tipo de archivo no valido.", "error")
            return redirect(url_for("associates.new_credential_form", associated_id = associated_id, current_page = current_page))
        newNameFile = save_photo_associated(extension, file)
    else:
        newNameFile = "sin-usuario.png"

    "Genera codigo qr"
    name_qr = save_qr_associated(associated_id)

    "Crea licencia"
    licenses.create_license(
        associated_id = associated_id,
        photo = newNameFile,
        qr = name_qr,
    )
    
    "Retorna a asociados"
    return redirect(url_for("associates.associated_index_page", num=current_page))


def create_credential_automatic(associated_id):
    "Obtengo la foto de perfil del usuario"
    name_photo = associates.get_associated_by_id(associated_id).user.photo
 
    "Genera codigo qr"
    name_qr = save_qr_associated(associated_id)

    "Crea licencia"
    licenses.create_license(
        associated_id = associated_id,
        photo = name_photo,
        qr = name_qr,
    )


@associated_blueprint.get("/delete/<associated_id>/<int:current_page>")
@token_required
@user_has_permission("associates_destroy")
def delete_associated_by_id(associated_id, current_page):
    """Recibe una id de un asociado y lo elimina de la base de datos validandolo."""
    associated_to_delete = associates.get_associated_by_id(associated_id)
    tiene_pagos = payments.find_payment_by_id_associated(associated_to_delete.id)
    if tiene_pagos and associated_to_delete.sports:
        flash(
            f"El asociado: {associated_id} no se puede eliminar porque tiene pagos y esta anotado en disciplinas.",
            "error",
        )
        return redirect(url_for("associates.associated_index_page", num=current_page))
    if tiene_pagos:
        flash(
            f"El asociado: {associated_id} no se puede eliminar porque tiene pagos.",
            "error",
        )
        return redirect(url_for("associates.associated_index_page", num=current_page))
    if associated_to_delete.sports:
        flash(
            f"El asociado: {associated_id} no se puede eliminar porque esta anotado en disciplinas",
            "error",
        )
        return redirect(url_for("associates.associated_index_page", num=current_page))
    associates.delete_associated(associated_to_delete)
    return redirect(url_for("associates.associated_index_page", num=1))


@associated_blueprint.post("/filtrar")
@token_required
@user_has_permission("associates_index")
def filtrar():
    """Filtra la lista de asociados por estado y/o apellido."""
    params = request.form
    if params["estado"] != "all" and params["surname"] != "":
        return redirect(
            url_for(
                "associates.filtrarApellidoEstado",
                estado=params["estado"],
                surname=params["surname"],
                num=1,
            )
        )
    if params["surname"] != "":
        return redirect(
            url_for("associates.filtrarApellido", surname=params["surname"], num=1)
        )
    if params["estado"] != "all":
        return redirect(
            url_for("associates.filtrarEstado", estado=params["estado"], num=1)
        )
    return redirect(url_for("associates.associated_index_page", num=1))


@associated_blueprint.get("/filtrar_apellido/<surname>/<int:num>")
@token_required
@user_has_permission("associates_index")
def filtrarApellido(surname, num):
    """Filtra la lista de asociados segun el apellido."""
    associated = associates.find_associated_by_surname(
        surname, setting.get_setting().cant_elements_page, num
    )
    if not associated.items:
        flash(f"El asociado: {surname} no existe", "error")
        return redirect(url_for("associates.associated_index_page", num=1))
    return render_template(
        "associates/associates.html",
        associates=associated,
        filterState=[True, "apellido", surname, ""],
    )


@associated_blueprint.get("/filtrar_apellido_estado/<surname>/<estado>/<int:num>")
@token_required
@user_has_permission("associates_index")
def filtrarApellidoEstado(estado, surname, num):
    """Filtra la lista de asociados segun el apellido y estado."""
    condition = corroborarEstado(estado)
    associated = associates.find_associated_by_surname_and_condition(
        surname, condition, setting.get_setting().cant_elements_page, num
    )
    if not associated.items:
        flash(
            f"El asociado: {surname} no existe o no se encuentra {condition}", "error"
        )
        return redirect(url_for("associates.associated_index_page", num=1))
    return render_template(
        "associates/associates.html",
        associates=associated,
        filterState=[True, "apellido_y_estado", surname, estado],
    )


@associated_blueprint.get("/filtrar_estado/<estado>/<int:num>")
@token_required
@user_has_permission("associates_index")
def filtrarEstado(estado, num):
    """Filtra la lista de asociados segun el estado."""
    condition = corroborarEstado(estado)
    associated = associates.find_associated_by_active(
        condition, num, setting.get_setting().cant_elements_page
    )
    if not associated.items:
        flash(f"No se encontraron asociados {estado}s", "info")
        return redirect(url_for("associates.associated_index_page", num=1))
    return render_template(
        "associates/associates.html",
        associates=associated,
        filterState=[True, "estado", "", estado],
    )


@associated_blueprint.get("/new/<int:current_page>")
@token_required
@user_has_permission("associates_new")
def new_associated_form(current_page):
    """Muestra formulario para agregar un asociado."""
    return render_template(
        "associates/new_associated.html", nav_menu=False, return_page=current_page
    )


@associated_blueprint.get("/carnet/detalles/<int:associated_id>/<int:current_page>")
@token_required
@user_has_permission("carnet_view")
def associated_license(associated_id, current_page):
    """Muestra el carnet del asociado con sus datos, foto y qr"""
    associated = associates.get_associated_by_id(associated_id)
    defaulter = associates.is_defaulter(associated_id)
    carnet = licenses.get_license_by_id(associated.credential[0].id)
    return render_template(
        "associates/associated_license.html",
        associated=associated,
        carnet=carnet,
        return_page=current_page,
        defaulter=defaulter
    )


@associated_blueprint.get("/carnet/<associated_id>/<int:current_page>")
@token_required
@user_has_permission("carnet_new")
def new_credential_form(associated_id, current_page):
    """Muestra formulario para generar un carnet a un asociado."""
    associated = associates.get_associated_by_id(associated_id)
    if not associated.user:
        return render_template(
            "associates/new_credential_associated.html", associated=associated, return_page=current_page
        )
    create_credential_automatic(associated_id)
    return redirect(url_for("associates.associated_index_page", num=current_page))

@associated_blueprint.get("/toggle/<int:associated_id>/<int:current_page>")
@token_required
@user_has_permission("sports_update")
def toggle_enable_associated_by_id(associated_id, current_page):
    """Recibe una id de asociado e invierte su condicion."""
    associated = associates.get_associated_by_id(associated_id)
    associated.sports.clear()
    if associated.condition == "Activo":
        associated.condition = "No-activo"
    else:
        associated.condition = "Activo"
    associates.update_associated(associated)
    return redirect(url_for("associates.associated_index_page", num=current_page))


@associated_blueprint.post("/update/<associated_id>/<int:current_page>")
@token_required
@user_has_permission("associates_update")
def update_associated(associated_id, current_page):
    """Actualiza los valores del asociado y redirecciona."""
    associated = associates.get_associated_by_id(associated_id)
    params = request.form
    result = associates.verify_edit_associated(params)
    if not result["success"]:
        flash(result["message"], "error")
        return render_template(
            "associates/edit_associated.html",
            associated=associated,
            return_page=current_page,
        )

    associated.name = params["name"]
    associated.surname = params["surname"]
    associated.gender = params["gender"]
    associated.direction = params["direction"]
    associated.phone = params["phone"]
    associated.mail = params["mail"]
    associates.update_associated(associated)

    flash(result["message"], "success")
    return redirect(url_for("associates.associated_index_page", num=current_page))


@associated_blueprint.get("/update/<associated_id>/<int:current_page>")
@token_required
@user_has_permission("associates_update")
def update_associated_form(associated_id, current_page):
    """Muetra el formulario para actualizar la informacion de un asociado."""
    associated = associates.get_associated_by_id(associated_id)
    return render_template(
        "associates/edit_associated.html",
        associated=associated,
        return_page=current_page,
    )


@associated_blueprint.get("/<associated_id>")
@token_required
@user_has_permission("associates_show")
def view(associated_id):
    """Obtiene y muestra un asociado."""
    associated = associates.get_associated_by_id(associated_id)
    return render_template(
        "associates/associates.html", associates=[associated], nav_menu=False
    )


@associated_blueprint.get("/<associated_id>/disciplinas/<current_page>")
@token_required
@user_has_permission("sports_index")
def list_sports_associated(associated_id, current_page):
    """Obtiene y muestra un asociado."""
    associated = associates.get_associated_by_id(associated_id)
    return render_template(
        "associates/associated_sports.html",
        associated_id=associated_id,
        sports=associated.sports,
        current_page=current_page,
    )


@associated_blueprint.get("/delete/<int:sport_id>/<int:associate_id>/<int:return_page>")
@user_has_permission("associates_update")
def delete_signup(sport_id, associate_id, return_page):
    """Elimina la inscripción de un asociado a una disciplina."""
    sport = sports.get_sport_by_id(sport_id)
    associate = associates.get_associated_by_id(associate_id)
    sports.delete_singup(sport, associate)
    return redirect(
        url_for(
            "associates.list_sports_associated",
            associated_id=associate_id,
            current_page=return_page,
        )
    )
