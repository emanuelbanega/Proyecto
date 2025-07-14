from flask import Blueprint, render_template, redirect, url_for, abort, flash

from src.core import setting
from src.core import sports
from src.core import associates
from src.core import setting
from src.web.helpers.auth import token_required, user_has_permission

signup_blueprint = Blueprint("signups", __name__, url_prefix="/inscripciones")


# Fuera de uso
# @signup_blueprint.get("/<int:sport_id>/<int:current_page>")
# @token_required
# @user_has_permission("signup_list")
# def signups_list(sport_id, current_page):
#     """Trae todos los inscriptos a una disciplina."""
#     sport_ret = sports.get_sport_by_id(sport_id)
#     return render_template(
#         "sports/signedup.html",
#         associates=sport_ret.associates,
#         sport_id=sport_id,
#         return_page=current_page,
#     )


@signup_blueprint.get("/<int:sport_id>/<int:return_page>/<int:associates_page>")
@token_required
@user_has_permission("signup_list")
def signups_list_page(sport_id, return_page, associates_page):
    """Trae los inscriptos a una disciplina paginados."""
    sport_ret = sports.get_sport_by_id(sport_id)
    associates_ret = associates.get_signed_associated(
        sport_ret, associates_page, setting.get_setting().cant_elements_page
    )
    return render_template(
        "sports/signedup.html",
        associates=associates_ret,
        sport_id=sport_id,
        return_page=return_page,
        associates_page=associates_page,
    )


@signup_blueprint.get(
    "/<int:sport_id>/<int:associate_id>/<int:return_page>/<int:associates_page>/<int:sign_page>"
)
@token_required
@user_has_permission("signup_new")
def sign_associate(sport_id, associate_id, return_page, associates_page, sign_page):
    """Inscribe un asociado a una discplina."""
    sport_ret = sports.get_sport_by_id(sport_id)
    sign = True
    if sport_ret.enabled is False:
        abort(404)

    associate_ret = associates.get_associated_by_id(associate_id)
    if associate_ret.condition == "No-activo":
        flash("El associado no esta activo.", "error")
        sign = False

    if associates.is_defaulter(associate_id):
        flash("El associado es moroso.", "error")
        sign = False

    if sport_ret in associate_ret.sports:
        flash("El associado ya se encuentra inscripto.", "error")
        sign = False

    if sign:
        sports.append_to_associates(sport_ret, associate_ret)
        flash("Inscripcion ralizada", "success")

    return redirect(
        url_for(
            "signups.sign_associate_form",
            sport_id=sport_id,
            return_page=return_page,
            associates_page=associates_page,
            sign_page=sign_page,
        )
    )


@signup_blueprint.get(
    "/new/<int:sport_id>/<int:return_page>/<int:associates_page>/<int:sign_page>"
)
@token_required
@user_has_permission("signup_new")
def sign_associate_form(sport_id, return_page, associates_page, sign_page):
    """Retorna los asociados para inscribir a una disciplina."""
    sport_ret = sports.get_sport_by_id(sport_id)
    if sport_ret.enabled is False:
        abort(404)
    associates_list = associates.get_unsigned_associated(
        sport_ret, sign_page, setting.get_setting().cant_elements_page
    )

    return render_template(
        "sports/sign_associate.html",
        sport=sport_ret,
        associates=associates_list,
        return_page=return_page,
        associates_page=associates_page,
    )


@signup_blueprint.get("/delete/<int:sport_id>/<int:associate_id>/<int:return_page>")
def delete_signup(sport_id, associate_id, return_page):
    """Elimina una inscripcion."""
    sport = sports.get_sport_by_id(sport_id)
    associate = associates.get_associated_by_id(associate_id)
    sports.delete_singup(sport, associate)
    return redirect(
        url_for(
            "signups.signups_list_page",
            sport_id=sport_id,
            return_page=return_page,
            associates_page=1,
        )
    )
