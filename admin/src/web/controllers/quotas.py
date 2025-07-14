from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash

from src.web.helpers.auth import token_required, user_has_permission
from src.core import quotas
from src.core import setting
from src.core import associates


quotas_blueprint = Blueprint("quotas", __name__, url_prefix="/cuotas")


@quotas_blueprint.get("/asociado/<int:id_associated>/pagina/<int:num_page>")
@token_required
@user_has_permission("quota_index")
def quotas_index_page(id_associated, num_page):
    """Muestra la lista de cuotas que tiene un asociado"""
    quotas_list = quotas.list_Quotas_Paged(
        id_associated,
        num_page,
        setting.get_setting().cant_elements_page,
    )
    return render_template(
        "quotas/quotas.html", quotas=quotas_list, id_associated=id_associated
    )


@quotas_blueprint.post("/asociado/<int:id_associated>/filtrar")
@token_required
@user_has_permission("quota_index")
def filtrar(id_associated):
    """Filtra la lista de cuotas por estado"""
    params = request.form
    if params["estado"] != "all":
        return redirect(
            url_for(
                "quotas.paginaFiltroEstado",
                id_associated=id_associated,
                state=params["estado"],
                num=1,
            )
        )
    return redirect(
        url_for("quotas.quotas_index_page", id_associated=id_associated, num_page=1)
    )


@quotas_blueprint.get(
    "/asociado/<int:id_associated>/filtrar_estado/<state>/pagina/<int:num>"
)
@token_required
@user_has_permission("quota_index")
def paginaFiltroEstado(id_associated, state, num):
    """Filtra la lista de usuario segun el estado"""

    quotas_list = quotas.find_quota_by_state(
        id_associated, state, num, setting.get_setting().cant_elements_page
    )
    if not quotas_list.items:
        flash(f"Sin resultados", "info")
    return render_template(
        "quotas/quotas.html",
        quotas=quotas_list,
        id_associated=id_associated,
        filterState=True,
        state=state,
    )


@quotas_blueprint.get(
    "/asociado/<int:id_associated>/detalle/<int:id_quota>/<int:current_page>"
)
@token_required
@user_has_permission("quota_show")
def quota_detail(id_associated, id_quota, current_page):
    """muestra la ventana con los datos del usuario"""
    quota = quotas.find_quota_by_id(id_quota)
    sportData = quotas.detail_quota(id_quota)
    tax = 0
    if not quota.state and quota.end_date < datetime.now():
        tax = sportData.total_amount * sportData.surcharge / 100
    return render_template(
        "quotas/quota_detail.html",
        id_associated=id_associated,
        quota=quota,
        sportData=sportData,
        tax=tax,
        return_page=current_page,
    )


@quotas_blueprint.get("/generar")
@token_required
@user_has_permission("quota_generate")
def quota_generate():
    """Genera las cuotas de los asociados"""
    listAssociates = associates.list_active_associated()
    if quotas.quota_generate(listAssociates):
        flash("Cuotas actualizadas", "success")
    return redirect(url_for("payments.payment_index_page", num=1))
