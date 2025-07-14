from flask import Blueprint, render_template, request
from flask import flash, redirect, url_for
from flask import session


from src.core import auth
from src.core import associates
from src.core import setting
from src.web.helpers.auth import token_required, user_has_permission, decode_token
from src.web.helpers import validate

user_blueprint = Blueprint("users", __name__, url_prefix="/usuarios")


@user_blueprint.get("/<int:num>")
@token_required
@user_has_permission("users_index")
def user_index(num):
    users = auth.list_Users_paginate(num, setting.get_setting().cant_elements_page)
    return render_template("user/users.html", users=users, filterState=False)


@user_blueprint.post("/filtrar")
@token_required
@user_has_permission("users_index")
def filtrar():
    """Filtra la lista de usuario por email y/o estado"""
    params = request.form
    if params["email"] != "":
        user = auth.find_user_by_mail(params["email"])
        if not user.items:
            flash(f"El email: {params['email']} no existe", "error")
            return redirect(url_for("users.user_index", num=1))
        return render_template("user/users.html", users=user)
    if params["estado"] != "all":
        return redirect(
            url_for("users.paginaFiltroEstado", state=params["estado"], num=1)
        )
    return redirect(url_for("users.user_index", num=1))


def corroborarEstado(estate):
    if estate == "bloqueado":
        return False
    return True


@user_blueprint.get("/filtrar_estado/<state>/<int:num>")
@token_required
@user_has_permission("users_index")
def paginaFiltroEstado(state, num):
    """Filtra la lista de usuario segun el estado"""
    # falta traer de configuración la cantidad de elementos a mostrar
    estado = corroborarEstado(state)
    users = auth.find_user_by_active(
        estado, num, setting.get_setting().cant_elements_page
    )
    if not users.items:
        flash(f"Sin resultados", "info")
    return render_template(
        "user/users.html", users=users, filterState=True, state=state
    )


@user_blueprint.get("/detalle/<int:user_id>/<int:current_page>")
@token_required
@user_has_permission("users_show")
def user_detail(user_id, current_page):
    """muestra la ventana con los datos del usuario"""
    user = auth.find_user_by_id(user_id)
    return render_template("user/user_detail.html", user=user, return_page=current_page)


@user_blueprint.get("/nuevo_usuario/<int:current_page>")
@token_required
@user_has_permission("users_new")
def new_user(current_page):
    """muestra la ventana del formulario para agregar un usuario"""
    return render_template("user/new_user.html", params=None, return_page=current_page)


@user_blueprint.route(
    "/modificar_usuario/<int:user_id>/<int:current_page>", methods=("GET", "POST")
)
@token_required
@user_has_permission("users_update")
def update_user(user_id, current_page):
    """muestra la ventana del formulario para modificar un usuario"""
    user = auth.find_user_by_id(user_id)
    if request.method == "POST":
        params = request.form
        if not validate.userName(params["userName"]):
            flash(
                "El nombre de Usuario solo puede contener numeros, letras y guion bajo",
                "error",
            )
            return render_template(
                "user/user_update.html", user=user, current_page=current_page
            )
        if not validate.name(params["first_name"]):
            flash("Nombre no valido", "error")
            return render_template(
                "user/user_update.html", user=user, current_page=current_page
            )
        if not validate.name(params["last_name"]):
            flash("Apellido no valido", "error")
            return render_template(
                "user/user_update.html", user=user, current_page=current_page
            )
        if params["password"] != "":
            result = validate.validatePassword(params["password"])
            if not result["user"]:
                flash(result["message"], "error")
                return render_template(
                    "user/new_user.html", params=params, return_page=current_page
                )
        result = auth.verify_update_user(params, user)
        if not result["user"]:
            flash(result["message"], "error")
            return render_template(
                "user/user_update.html", user=user, current_page=current_page
            )
        flash(result["message"], "success")
        return redirect(
            url_for("users.user_detail", user_id=user.id, current_page=current_page)
        )
    return render_template(
        "user/user_update.html", user=user, current_page=current_page
    )


@user_blueprint.post("/nuevo_usuario/<int:current_page>")
@token_required
@user_has_permission("users_new")
def add_user(current_page):
    """verifica los datos del nuevo usuario y lo agrega"""
    params = request.form
    if not validate.email(params["email"]):
        flash("Correo no válido", "error")
        return render_template(
            "user/new_user.html", params=params, return_page=current_page
        )

    if not validate.userName(params["userName"]):
        flash(
            "El nombre de Usuario solo puede contener numeros, letras y guion bajo",
            "error",
        )
        return render_template(
            "user/new_user.html", params=params, return_page=current_page
        )

    if not validate.name(params["first_name"]):
        flash("Nombre no valido", "error")
        return render_template(
            "user/new_user.html", params=params, return_page=current_page
        )

    if not validate.name(params["last_name"]):
        flash("Apellido no valido", "error")
        return render_template(
            "user/new_user.html", params=params, return_page=current_page
        )
    result = validate.validatePassword(params["password"])
    if not result["user"]:
        flash(result["message"], "error")
        return render_template(
            "user/new_user.html", params=params, return_page=current_page
        )

    result = auth.verify_new_user(params)

    if not result["user"]:
        flash(result["message"], "error")
        return render_template(
            "user/new_user.html", params=params, return_page=current_page
        )
    flash(result["message"], "success")
    return redirect(
        url_for(
            "users.user_detail",
            user_id=result["user"].id,
            current_page=current_page,
        )
    )


@user_blueprint.get("/alternar_activo/<int:user_id>/<int:pag_actual>")
@token_required
@user_has_permission("users_update")
def toggle_blocked(user_id, pag_actual):
    """Alterna el bloqueo a un usuario no administrador"""
    result = auth.block_user(user_id)
    if not result["user"]:
        flash(result["message"], "error")
        return redirect(url_for("users.user_index", num=pag_actual))
    flash(result["message"], "success")
    return redirect(url_for("users.user_index", num=pag_actual))


@user_blueprint.post("/roles/<int:user_id>/<int:current_page>")
@token_required
@user_has_permission("users_update")
def asig_role(user_id, current_page):
    """muestra la ventana con los datos del usuario"""
    user = auth.find_user_by_id(user_id)
    params = request.form
    roles = auth.list_Roles()
    email_logged_in = decode_token(session["user"])["user"]
    asigSocio = False
    for role in roles:
        if role.name in params:
            if role.name == "socio" and not role in user.role:
                asigSocio = True
            else:
                auth.assign_role(user, role)
        elif role.name == "administrador" and user.email == email_logged_in:
            flash("No puedes quitarte el rol administrador a vos mismo", "error")
            return render_template(
                "user/user_detail.html", user=user, return_page=current_page
            )
        elif role.name == "socio" and user.associated:
            flash(
                "No puedes quitarle el rol socio, el usuario tiene asociados vinculados",
                "error",
            )
            return render_template(
                "user/user_detail.html", user=user, return_page=current_page
            )
        elif role in user.role:
            auth.remove_user_role(user, role)
    if asigSocio:
        return redirect(
            url_for(
                "users.listAssociates",
                user_id=user_id,
                num=1,
                current_page=current_page,
            )
        )
    flash("Roles actualizados", "success")
    return render_template("user/user_detail.html", user=user, return_page=current_page)


@user_blueprint.get("/eliminar/<int:user_id>/<int:current_page>")
@token_required
@user_has_permission("users_destroy")
def delete_user_by_id(user_id, current_page):
    """Recibe una id de disciplina y la elimina de la BD."""
    result = auth.delete_by_id(user_id)
    if not result["user"]:
        flash(result["message"], "error")
        return redirect(url_for("users.user_index", num=current_page))
    flash(result["message"], "success")
    return redirect(url_for("users.user_index", num=current_page))


@user_blueprint.get("/<int:user_id>/associados/pagina/<int:num>")
@token_required
@user_has_permission("users_update")
def listAssociates(user_id, num):
    """Muestra la lista de asociados disponibles para asignar al usuario socio"""
    listAssociates = associates.list_associates_no_user(
        num, setting.get_setting().cant_elements_page
    )
    return render_template(
        "user/asig_associated.html",
        user_id=user_id,
        associates=listAssociates,
    )


@user_blueprint.get(
    "/<int:user_id>/asignar_asociado/<int:associated_id>/<int:current_page>"
)
@token_required
@user_has_permission("users_update")
def asig_associate(user_id, associated_id, current_page):
    """verifica que un asociado puede agregar la relacion con el socio"""
    user = auth.find_user_by_id(user_id)
    associate = associates.get_associated_by_id(associated_id)
    if associate is None:
        flash("Asociado no existente", "error")
        return redirect(
            url_for(
                "users.listAssociates",
                user_id=user_id,
                num=current_page,
            )
        )
    result = auth.verify_asig_associate(user, associate)
    if not result["user"]:
        flash(result["message"], "error")
        return redirect(
            url_for("users.listAssociates", user_id=user_id, num=current_page)
        )
    role = auth.find_role_by_name("socio")
    auth.assign_role(user, role)
    flash(result["message"], "success")
    return render_template(
        "user/user_detail.html",
        user=result["user"],
        return_page=1,
    )


@user_blueprint.get("/<int:user_id>/asociado/borrar/<int:current_page>")
@token_required
@user_has_permission("users_update")
def remove_associate(user_id, current_page):
    """Elimina la relacion entre el asociado y el usuario"""
    user = auth.find_user_by_id(user_id)
    if not user.associated:
        flash("El usuario no tiene asociado", "error")
        return render_template(
            "user/user_detail.html", user=user, return_page=current_page
        )
    associates.remove_associate_user(user.associated[0])
    role = auth.find_role_by_name("socio")
    auth.remove_user_role(user, role)
    flash("Usuario actualizado", "success")
    return render_template("user/user_detail.html", user=user, return_page=current_page)
