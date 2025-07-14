from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

from src.core import sports
from src.core import setting
from src.web.helpers.auth import token_required, user_has_permission

sport_blueprint = Blueprint("sports", __name__, url_prefix="/disciplinas")


@sport_blueprint.get("/")
@token_required
@user_has_permission("users_index")
def sport_index():
    """Obtiene y muestra todas las discplinas."""
    sports_list = sports.list_sports()
    return render_template("sports/sports.html", sports=sports_list)


@sport_blueprint.get("/<int:num>")
@token_required
@user_has_permission("sports_index")
def sport_index_page(num):
    """Trae disciplinas paginadas."""
    sports_list = sports.list_sports_page(num, setting.get_setting().cant_elements_page)
    return render_template(
        "sports/sports.html",
        sports=sports_list,
        currency=setting.get_setting().currency_type,
    )


@sport_blueprint.post("/filtered/<int:num>")
@token_required
@user_has_permission("sports_index")
def sport_index_page_filter(num):
    """Procesa parametros y genera request de filtrado."""
    params = request.form
    if params["estado"] == "habilitada":
        enabled = True
    elif params["estado"] == "deshabilitada":
        enabled = False
    else:
        enabled = "None"

    if params["name"] != "":
        name = params["name"]
    else:
        name = "None"

    return redirect(
        url_for("sports.sport_index_page_filtered", num=num, name=name, enabled=enabled)
    )


@sport_blueprint.get("/filtered/<int:num>/<name>/<enabled>")
@token_required
@user_has_permission("sports_index")
def sport_index_page_filtered(num, name, enabled):
    """Filtra segun los parametros y devuelve disciplinas paginadas."""
    if name == "None":
        name = None

    if enabled == "None":
        enabled = None

    sports_list = sports.list_sports_page_filtered(
        num, setting.get_setting().cant_elements_page, enabled, name
    )

    return render_template(
        "sports/sports.html",
        sports=sports_list,
        currency=setting.get_setting().currency_type,
        filters={"name": str(name), "enabled": str(enabled)},
    )


# No funciona por ahora
# @sport_blueprint.get("/detalle/<sport_id>")
# @token_required
# @user_has_permission("sports_show")
# def view(sport_id):
#     """Obtiene y muestra una discplina."""
#     sport = sports.get_sport_by_id(sport_id)
#     return render_template("sports/sports.html", sports=[sport])


@sport_blueprint.get("/new/<int:current_page>")
@token_required
@user_has_permission("sports_new")
def new_sport_form(current_page):
    """Muestra formulario para agregar una disciplina."""
    return render_template("sports/new_sport.html", return_page=current_page)


@sport_blueprint.post("/new/<int:current_page>")
@token_required
@user_has_permission("sports_new")
def add_sport(current_page):
    """Recibe datos y crea una nueva discplina. Luego Redirecciona."""
    params = request.form
    enable = True
    if request.form.get("enabled") is None:
        enable = False

    result = sports.verify_new_sport(params, enable)
    if not result["sport"]:
        flash(result["message"], "error")
        # return redirect(url_for("sports.new_sport_form"))
        return render_template(
            "sports/new_sport.html", placeholder=params, return_page=current_page
        )

    flash(result["message"], "success")
    return redirect(url_for("sports.sport_index_page", num=current_page))


@sport_blueprint.get("/delete/<sport_id>/<int:current_page>")
@token_required
@user_has_permission("sports_destroy")
def delete_sport_by_id(sport_id, current_page):
    """Recibe una id de disciplina y la elimina de la BD."""
    sport_to_delete = sports.get_sport_by_id(sport_id)
    if sport_to_delete.associates:
        message = "La disciplina tiene inscriptos"
        flash(message, "error")
        return redirect(url_for("sports.sport_index_page", num=current_page))

    sports.delete_sport(sport_to_delete)
    message = "Disciplinas eliminada correctamente"
    flash(message, "success")
    # Como vuelvo a la pagina en la que estaba si la pagina se elimino?
    return redirect(url_for("sports.sport_index_page", num=1))


@sport_blueprint.get("/toggle/<int:sport_id>/<int:current_page>")
@token_required
@user_has_permission("sports_update")
def toggle_enable_sport_by_id(sport_id, current_page):
    """Recibe una id de sport e invierte "habilitado"."""
    sport = sports.get_sport_by_id(sport_id)
    sports.delete_all_signed(sport)
    sports.invert_sport_enabled(sport)
    sports.update_sport(sport)
    return redirect(url_for("sports.sport_index_page", num=current_page))


@sport_blueprint.get("/update/<sport_id>/<int:current_page>")
@token_required
@user_has_permission("sports_update")
def update_sport_form(sport_id, current_page):
    """Muetra el formulario para actualizar la informacion de una disciplina."""
    sport = sports.get_sport_by_id(sport_id)
    return render_template(
        "sports/edit_sport.html", sport=sport, return_page=current_page
    )


@sport_blueprint.post("/update/<sport_id>/<int:current_page>")
@token_required
@user_has_permission("sports_update")
def update_sport(sport_id, current_page):
    """Actualiza los valores de la disciplina y redirecciona."""
    sport = sports.get_sport_by_id(sport_id)
    params = request.form
    result = sports.verify_edit_sport(params, sport)
    if not result["success"]:
        flash(result["message"], "error")
        return render_template(
            "sports/edit_sport.html", sport=sport, return_page=current_page
        )

    sport.name = params["sportName"]
    sport.division = params["division"]
    sport.instructors_names = params["instructors"]
    sport.schedule = params["schedule"]
    sport.monthly_fee = params["fee"].replace(".", "")
    sports.update_sport(sport)

    flash(result["message"], "success")
    return redirect(url_for("sports.sport_index_page", num=current_page))
