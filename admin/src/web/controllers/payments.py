from flask import Blueprint, render_template, request, redirect, url_for, flash

from src.core import setting
from src.core import payments
from src.web.helpers.auth import token_required, user_has_permission
from src.core.quotas.quotaV2 import (
    Quota,
    get_quota_by_id,
    get_quotas,
    QuotaJson,
    get_detail_quota,
    assign_payment,
)
from src.core import payments, associates
import json
from datetime import datetime


payment_blueprint = Blueprint("payments", __name__, url_prefix="/pagos")


@payment_blueprint.get("/<int:num>")
@token_required
@user_has_permission("quota_index")
def payment_index_page(num):
    # Trae asociados paginadas.
    payments_list = payments.list_payments_page(
        num, setting.get_setting().cant_elements_page
    )
    return render_template(
        "payments/payments.html",
        payments=payments_list,
        currency=setting.get_setting().currency_type,
    )


@payment_blueprint.get("/new_payment/<int:current_page>")
@token_required
@user_has_permission("quota_new")
def new_payment(current_page):
    associates_list = associates.list_associated()
    return render_template(
        "payments/new_payment.html",
        associates=associates_list,
        quotas=[],
        selected=0,
        return_page=current_page,
    )


@payment_blueprint.post("/new_payment/<int:current_page>/filtrar")
@token_required
@user_has_permission("quota_new")
def filtrar_quotas(current_page):
    params = request.form
    associated_id = int(params["selectAsociado"])
    associates_list = associates.list_associated()
    quotas_list = []
    quotas = get_quotas()
    for i in quotas:
        if i.associated_id == associated_id and i.state == False:
            quota_parsed = QuotaJson.fromJSON(i.dataJSON)
            i.final_amount = quota_parsed.total_amount
            if i.end_date < datetime.now():
                amount_extra = quota_parsed.surcharge * quota_parsed.total_amount / 100
                i.final_amount = i.final_amount + amount_extra
            quotas_list.append(i)
    return render_template(
        "payments/new_payment.html",
        associates=associates_list,
        quotas=quotas_list,
        selected=associated_id,
        return_page=current_page,
    )


@payment_blueprint.get("/new_payment/<int:current_page>/pagar/<int:quotaId>")
@token_required
@user_has_permission("quota_new")
def pagar(current_page, quotaId):
    quota = get_quota_by_id(quotaId)
    quota_detail = get_detail_quota(quotaId)
    overdue_fee = quota.end_date > datetime.now()
    amount_extra = quota_detail.surcharge * quota_detail.total_amount / 100
    return render_template(
        "payments/payment_pay.html",
        current_page=current_page,
        quota=quota_detail,
        id_quota=quotaId,
        overdue_fee=overdue_fee,
        amount_extra=amount_extra,
    )


@payment_blueprint.post("/new_payment/<int:current_page>/pagar/<int:quotaId>")
@token_required
@user_has_permission("quota_new")
def pagar_post(current_page, quotaId):
    quota_from_db = get_quota_by_id(quotaId)
    if quota_from_db.state:
        flash("La cuota ya esta pagada")
        return redirect(url_for("payments.payment_index_page", num=current_page))
    quota_parsed = QuotaJson.fromJSON(quota_from_db.dataJSON)
    if quota_from_db.end_date < datetime.now():
        amount_extra = quota_parsed.surcharge * quota_parsed.total_amount / 100
        quota_parsed.total_amount = quota_parsed.total_amount + amount_extra
    payment = payments.add_payment(
        orden=quota_from_db.id + 1000, 
        amount=quota_parsed.total_amount,
        state=True
    )
    assign_payment(quota_from_db, payment)
    flash("Se registro el pago correctamente", "success")
    return redirect(url_for("payments.payment_index_page", num=current_page))


@payment_blueprint.post("/filtrar/<int:current_page>")
@token_required
@user_has_permission("quota_index")
def filtrar(current_page):
    # Filtra la lista de pagos segun el numero de socio o apellido.
    params = request.form
    if params["id"] != "" and int(params["id"]) > 0:
        payments_list = payments.find_payment_by_id(
            int(params["id"]), setting.get_setting().cant_elements_page, current_page
        )
        if not payments_list.items:
            flash(
                f"No se encuentra pagos del asociado con numero de socio: {params['id']}",
                "error",
            )
            return redirect(url_for("payments.payment_index_page", num=1))
        return render_template("payments/payments.html", payments=payments_list)
    if params["surname"] != "":
        payments_list = payments.find_payment_by_surname(
            params["surname"], setting.get_setting().cant_elements_page, current_page
        )
        if not payments_list.items:
            flash(f"No se encuentra pagos del asociado: {params['surname']}", "error")
            return redirect(url_for("payments.payment_index_page", num=1))
        return render_template("payments/payments.html", payments=payments_list)

    return redirect(url_for("payments.payment_index_page", num=1))


@payment_blueprint.get("/detail/<int:current_page><int:payment_id>")
@token_required
@user_has_permission("quota_show")
def recibo(current_page, payment_id):
    payment = payments.get_payment_by_id(payment_id)
    currency_type = QuotaJson.fromJSON(payment.quotas[0].dataJSON).currency_type
    return render_template(
        "payments/payment_detail.html",
        currency_type=currency_type,
        current_page=current_page,
        payment=payment,
        title=setting.get_setting().voucher_title,
    )

@payment_blueprint.get("/pending_payments/<int:current_page>")
@token_required
@user_has_permission("quota_new")
def pending_payments(current_page):
    pending_payments_list = payments.get_pending_payments()
    empty = True
    for _ in pending_payments_list:
        empty = False
        break
    return render_template(
        "payments/pending_payments.html",
        return_page=current_page,
        pending_payments=pending_payments_list,
        empty=empty
    )

@payment_blueprint.post("/pending_payments/<int:current_page>/<int:pagoId>")
@token_required
@user_has_permission("quota_new")
def aprobar_pago(current_page, pagoId):
    current_payment = payments.get_payment_by_id(pagoId)
    print(current_payment.amount)
    payments.confirm_payment(current_payment)
    flash("Se registro el pago correctamente", "success")
    return redirect(url_for("payments.payment_index_page", num=current_page))

@payment_blueprint.post("/pending_payments/rechazar/<int:current_page>/<int:pagoId>")
@token_required
@user_has_permission("quota_new")
def rechazar_pago(current_page, pagoId):
    current_payment = payments.get_payment_by_id(pagoId)
    payments.decline_payment(current_payment)
    flash("Se rechazo el pago", "success")
    return redirect(url_for("payments.payment_index_page", num=current_page))